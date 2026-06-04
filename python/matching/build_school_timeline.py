"""Build signing vs development program attribution per recruit."""
import pandas as pd
from rapidfuzz import fuzz, process

from python.ingest.config import RAW_DIR, STAGING_DIR
from python.ingest.io import write_parquet
from python.ingest.normalize import normalize_name, player_key
from python.matching.build_player_bridge import MAX_YEARS_TO_DRAFT

FUZZY_THRESHOLD = 92


def program_key_from_school(value: object) -> str:
    return normalize_name(value)


def load_recruits() -> pd.DataFrame:
    df = pd.read_parquet(RAW_DIR / "recruits.parquet")
    df["player_key"] = df["player_name"].map(player_key)
    df["name_norm"] = df["player_name"].map(normalize_name)
    df["signing_program_key"] = df["program"].map(program_key_from_school)
    return df


def load_transfers() -> pd.DataFrame:
    path = RAW_DIR / "transfers.parquet"
    if not path.exists():
        return pd.DataFrame(
            columns=[
                "season",
                "first_name",
                "last_name",
                "origin",
                "destination",
                "transfer_date",
                "player_key",
                "name_norm",
                "destination_program_key",
            ]
        )
    df = pd.read_parquet(path)
    df["player_name"] = (
        df["first_name"].astype(str).str.strip() + " " + df["last_name"].astype(str).str.strip()
    )
    df["player_key"] = df["player_name"].map(player_key)
    df["name_norm"] = df["player_name"].map(normalize_name)
    df["destination_program_key"] = df["destination"].map(program_key_from_school)
    return df


def development_from_transfers(matched: pd.DataFrame, signing: str) -> tuple[str, str, int]:
    if matched.empty:
        return signing, "no_transfer", 0

    ordered = matched.sort_values(
        by=["season", "transfer_date"],
        ascending=[True, True],
        na_position="first",
    )
    last = ordered.iloc[-1]
    dest = last["destination_program_key"]
    if not dest:
        return signing, "unmatched_transfer", len(matched)

    return dest, "last_destination", len(matched)


def build_timeline(recruits: pd.DataFrame, transfers: pd.DataFrame) -> pd.DataFrame:
    if transfers.empty:
        rows = []
        for _, recruit in recruits.iterrows():
            signing = recruit["signing_program_key"] or program_key_from_school(recruit["program"])
            rows.append(
                {
                    "player_key": recruit["player_key"],
                    "class_year": int(recruit["class_year"]),
                    "signing_program_key": signing,
                    "development_program_key": signing,
                    "transfer_count": 0,
                    "attribution_rule": "no_transfer",
                    "is_transfer": False,
                }
            )
        return pd.DataFrame(rows)

    rows: list[dict] = []

    for _, recruit in recruits.iterrows():
        signing = recruit["signing_program_key"] or program_key_from_school(recruit["program"])
        class_year = int(recruit["class_year"])
        draft_window_end = class_year + MAX_YEARS_TO_DRAFT

        pool = transfers[
            (transfers["season"] >= class_year) & (transfers["season"] <= draft_window_end)
        ]

        matched = pool.iloc[0:0]
        r_key = recruit["player_key"]
        if r_key and not pool.empty:
            matched = pool[pool["player_key"] == r_key]

        if matched.empty and recruit["name_norm"] and not pool.empty:
            pool_names = pool["name_norm"].dropna().unique().tolist()
            if pool_names:
                hit = process.extractOne(
                    recruit["name_norm"],
                    pool_names,
                    scorer=fuzz.token_sort_ratio,
                    score_cutoff=FUZZY_THRESHOLD,
                )
                if hit:
                    matched = pool[pool["name_norm"] == hit[0]]

        dev, rule, transfer_count = development_from_transfers(matched, signing)
        rows.append(
            {
                "player_key": r_key,
                "class_year": class_year,
                "signing_program_key": signing,
                "development_program_key": dev,
                "transfer_count": transfer_count,
                "attribution_rule": rule,
                "is_transfer": signing != dev,
            }
        )

    out = pd.DataFrame(rows)
    for col in ("player_key", "signing_program_key", "development_program_key", "attribution_rule"):
        out[col] = out[col].astype("string")
    out["class_year"] = out["class_year"].astype("Int64")
    out["transfer_count"] = out["transfer_count"].astype("Int64")
    out["is_transfer"] = out["is_transfer"].astype("bool")
    return out.drop_duplicates(subset=["player_key", "class_year"], keep="first")


def main() -> None:
    recruits = load_recruits()
    transfers = load_transfers()
    timeline = build_timeline(recruits, transfers)
    write_parquet(timeline, STAGING_DIR / "player_school_timeline.parquet")

    transfer_rate = timeline["is_transfer"].mean() if len(timeline) else 0
    print(f"Wrote {len(timeline):,} timeline rows")
    print(f"Transfer attribution rate: {transfer_rate:.1%}")


if __name__ == "__main__":
    main()
