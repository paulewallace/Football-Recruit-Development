"""Pull NFL draft picks from nflverse (nfl_data_py)."""
import pandas as pd

try:
    import nfl_data_py as nfl
except ImportError as exc:
    raise ImportError("Install nfl_data_py: pip install nfl_data_py") from exc

from python.ingest.config import DRAFT_YEAR_END, DRAFT_YEAR_START, RAW_DIR
from python.ingest.io import write_parquet


def main() -> None:
    years = list(range(DRAFT_YEAR_START, DRAFT_YEAR_END + 1))
    raw = nfl.import_draft_picks(years)

    # nflverse column names vary slightly by season; map defensively.
    name_col = "pfr_player_name" if "pfr_player_name" in raw.columns else "player_name"
    if name_col not in raw.columns:
        raise KeyError(f"No player name column in draft data: {raw.columns.tolist()}")

    season_col = "season" if "season" in raw.columns else "draft_year"
    round_col = "round" if "round" in raw.columns else "draft_round"
    pick_col = "pick" if "pick" in raw.columns else "draft_pick_overall"
    team_col = "team" if "team" in raw.columns else "nfl_team"
    college_col = "college" if "college" in raw.columns else None

    df = pd.DataFrame(
        {
            "player_name": raw[name_col].astype("string"),
            "draft_year": pd.to_numeric(raw[season_col], errors="coerce").astype("Int64"),
            "draft_round": pd.to_numeric(raw[round_col], errors="coerce").astype("Int64"),
            "draft_pick_overall": pd.to_numeric(raw[pick_col], errors="coerce").astype("Int64"),
            "nfl_team": raw[team_col].astype("string") if team_col in raw.columns else pd.NA,
            "college": raw[college_col].astype("string") if college_col else pd.NA,
        }
    )
    df = df.dropna(subset=["player_name", "draft_year"])
    df = df.drop_duplicates(subset=["player_name", "draft_year"], keep="first")

    write_parquet(df, RAW_DIR / "nfl_draft.parquet")


if __name__ == "__main__":
    main()
