"""Parquet I/O with explicit dtypes for DuckDB staging."""
from pathlib import Path

import pandas as pd


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    print(f"Wrote {path} ({len(df):,} rows)")
