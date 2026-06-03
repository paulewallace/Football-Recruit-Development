"""Pull high-school recruiting classes from CollegeFootballData.com."""
import pandas as pd

from python.ingest.cfbd_client import fetch_recruits
from python.ingest.config import CLASS_YEAR_END, CLASS_YEAR_START, RAW_DIR
from python.ingest.io import write_parquet


def main() -> None:
    frames: list[pd.DataFrame] = []
    for year in range(CLASS_YEAR_START, CLASS_YEAR_END + 1):
        chunk = fetch_recruits(year)
        print(f"  {year}: {len(chunk):,} recruits")
        if not chunk.empty:
            frames.append(chunk)

    if not frames:
        raise RuntimeError("No recruiting rows returned. Check API key and year range.")

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset=["player_name", "program", "class_year"], keep="first")

    for col in ("player_name", "program", "position"):
        df[col] = df[col].astype("string")
    for col in ("class_year", "star_rating", "national_rank"):
        df[col] = df[col].astype("Int64")

    write_parquet(df, RAW_DIR / "recruits.parquet")


if __name__ == "__main__":
    main()
