"""Build canonical program reference from CFBD teams + recruiting data."""
import pandas as pd
import requests

from python.ingest.cfbd_client import _headers
from python.ingest.config import CFBD_BASE_URL, RAW_DIR, get_cfbd_api_key
from python.ingest.io import write_parquet
from python.ingest.normalize import normalize_name


def fetch_teams() -> pd.DataFrame:
    response = requests.get(
        f"{CFBD_BASE_URL}/teams",
        headers=_headers(),
        timeout=60,
    )
    response.raise_for_status()
    rows = response.json()
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["program", "program_key", "conference"])

    return pd.DataFrame(
        {
            "program": df["school"].astype("string"),
            "program_key": df["school"].map(normalize_name).astype("string"),
            "conference": df.get("conference", pd.Series(dtype="string")).astype("string"),
        }
    ).drop_duplicates(subset=["program_key"])


def main() -> None:
    _ = get_cfbd_api_key()
    teams = fetch_teams()

    recruits_path = RAW_DIR / "recruits.parquet"
    if recruits_path.exists():
        recruits = pd.read_parquet(recruits_path)
        from_recruits = pd.DataFrame(
            {
                "program": recruits["program"].astype("string"),
                "program_key": recruits["program"].map(normalize_name).astype("string"),
                "conference": pd.NA,
            }
        ).drop_duplicates(subset=["program_key"])
        programs = pd.concat([teams, from_recruits], ignore_index=True)
        programs = programs.drop_duplicates(subset=["program_key"], keep="first")
    else:
        programs = teams

    write_parquet(programs, RAW_DIR / "programs.parquet")


if __name__ == "__main__":
    main()
