"""DuckDB query helper for warehouse marts."""
from pathlib import Path
from typing import Any, Optional

import duckdb
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "warehouse" / "college_dev.duckdb"


def connect(read_only: bool = True) -> duckdb.DuckDBPyConnection:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Warehouse not found at {DB_PATH}. Run `make transform` from the project root."
        )
    return duckdb.connect(str(DB_PATH), read_only=read_only)


def query(sql: str, params: Optional[dict[str, Any]] = None) -> pd.DataFrame:
    """Run SQL and return a DataFrame. Use $name placeholders, e.g. `$min_recruits`."""
    with connect(read_only=True) as conn:
        return conn.execute(sql, params or {}).df()


def list_tables() -> pd.DataFrame:
    return query("SHOW TABLES")
