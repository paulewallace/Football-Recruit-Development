"""Match recruits to NFL draft outcomes (deterministic + fuzzy)."""
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz

from python.ingest.config import RAW_DIR, STAGING_DIR
from python.ingest.io import write_parquet
from python.ingest.normalize import normalize_name, player_key

# Typical NFL draft window after HS signing class.
MIN_YEARS_TO_DRAFT = 3
MAX_YEARS_TO_DRAFT = 6
FUZZY_THRESHOLD = 92


def load_recruits() -> pd.DataFrame:
    df = pd.read_parquet(RAW_DIR / "recruits.parquet")
    df["player_key"] = df["player_name"].map(player_key)
    df["name_norm"] = df["player_name"].map(normalize_name)
    return df


def load_draft() -> pd.DataFrame:
    df = pd.read_parquet(RAW_DIR / "nfl_draft.parquet")
    df["player_key"] = df["player_name"].map(player_key)
    df["name_norm"] = df["player_name"].map(normalize_name)
    return df


def match_players(recruits: pd.DataFrame, draft: pd.DataFrame) -> pd.DataFrame:
    matches: list[dict] = []
    used_draft_idx: set[int] = set()

    draft_by_key = draft.groupby("player_key", dropna=False)

    for _, recruit in recruits.iterrows():
        r_key = recruit["player_key"]
        if not r_key:
            continue

        class_year = int(recruit["class_year"])
        draft_window = draft[
            (draft["draft_year"] >= class_year + MIN_YEARS_TO_DRAFT)
            & (draft["draft_year"] <= class_year + MAX_YEARS_TO_DRAFT)
        ]

        candidate = None
        rule = None
        confidence = None

        if r_key in draft_by_key.groups:
            pool = draft_by_key.get_group(r_key)
            pool = pool[~pool.index.isin(used_draft_idx)]
            if not pool.empty:
                candidate = pool.iloc[0]
                rule = "exact_player_key"
                confidence = "high"

        if candidate is None and recruit["name_norm"]:
            best_score = 0
            best_row = None
            for idx, row in draft_window.iterrows():
                if idx in used_draft_idx:
                    continue
                score = fuzz.token_sort_ratio(recruit["name_norm"], row["name_norm"])
                if score > best_score:
                    best_score = score
                    best_row = row
            if best_row is not None and best_score >= FUZZY_THRESHOLD:
                candidate = best_row
                rule = "fuzzy_name_year_window"
                confidence = "medium"

        if candidate is None:
            continue

        used_draft_idx.add(candidate.name)
        matches.append(
            {
                "player_key": r_key,
                "recruit_player_name": recruit["player_name"],
                "draft_player_name": candidate["player_name"],
                "program_key": normalize_name(recruit["program"]),
                "class_year": class_year,
                "draft_year": int(candidate["draft_year"]),
                "match_confidence": confidence,
                "match_rule": rule,
            }
        )

    if not matches:
        return pd.DataFrame(
            columns=[
                "player_key",
                "recruit_player_name",
                "draft_player_name",
                "program_key",
                "class_year",
                "draft_year",
                "match_confidence",
                "match_rule",
            ]
        )

    out = pd.DataFrame(matches)
    for col in ("player_key", "recruit_player_name", "draft_player_name", "program_key", "match_confidence", "match_rule"):
        out[col] = out[col].astype("string")
    for col in ("class_year", "draft_year"):
        out[col] = out[col].astype("Int64")
    return out


def export_unmatched(recruits: pd.DataFrame, bridge: pd.DataFrame) -> None:
    matched_keys = set(bridge["player_key"].tolist()) if not bridge.empty else set()
    unmatched = recruits[~recruits["player_key"].isin(matched_keys)]
    path = STAGING_DIR / "unmatched_recruits.parquet"
    if unmatched.empty:
        print("No unmatched recruits to export.")
        return
    write_parquet(
        unmatched[
            ["player_name", "program", "class_year", "star_rating", "position"]
        ].copy(),
        path,
    )


def main() -> None:
    recruits = load_recruits()
    draft = load_draft()
    bridge = match_players(recruits, draft)
    write_parquet(bridge, STAGING_DIR / "player_bridge.parquet")
    export_unmatched(recruits, bridge)
    print(f"Matched {len(bridge):,} / {len(recruits):,} recruits ({len(bridge) / len(recruits):.1%})")


if __name__ == "__main__":
    main()
