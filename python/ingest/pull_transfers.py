"""Pull transfer portal entries from CollegeFootballData.com."""
import pandas as pd

from python.ingest.cfbd_client import fetch_transfers
from python.ingest.config import RAW_DIR, TRANSFER_YEAR_END, TRANSFER_YEAR_START
from python.ingest.io import write_parquet


def main() -> None:
    frames: list[pd.DataFrame] = []
    for year in range(TRANSFER_YEAR_START, TRANSFER_YEAR_END + 1):
        chunk = fetch_transfers(year)
        print(f"  {year}: {len(chunk):,} portal entries")
        if not chunk.empty:
            frames.append(chunk)

    if not frames:
        raise RuntimeError("No transfer portal rows returned. Check API key and year range.")

    df = pd.concat(frames, ignore_index=True)
    for col in ("first_name", "last_name", "position", "origin", "destination"):
        df[col] = df[col].astype("string")
    for col in ("season", "stars"):
        df[col] = df[col].astype("Int64")

    write_parquet(df, RAW_DIR / "transfers.parquet")


if __name__ == "__main__":
    main()
