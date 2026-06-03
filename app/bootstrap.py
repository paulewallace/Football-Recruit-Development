"""Streamlit / cloud bootstrap: project root on sys.path and warehouse check."""
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "warehouse" / "college_dev.duckdb"

REQUIRED_RAW = (
    "recruits.parquet",
    "nfl_draft.parquet",
    "programs.parquet",
)


def setup_path() -> Path:
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    return PROJECT_ROOT


def raw_data_ready() -> bool:
    return all((RAW_DIR / name).exists() for name in REQUIRED_RAW)


def ensure_warehouse() -> None:
    """Build DuckDB warehouse from committed Parquet if the DB file is missing."""
    if DB_PATH.exists():
        return
    if not raw_data_ready():
        return
    from python.run_transform import main as run_transform

    run_transform()


def warehouse_status_message() -> Optional[str]:
    if DB_PATH.exists():
        return None
    if raw_data_ready():
        return (
            "Warehouse file missing. Raw Parquet was found — "
            "run `make transform` locally and commit `warehouse/college_dev.duckdb`, "
            "or rebuild on deploy once bootstrap runs."
        )
    return (
        "Warehouse file missing and raw Parquet is not in the repo. "
        "For Streamlit Cloud, commit `warehouse/college_dev.duckdb` "
        "(and optionally `data/raw/*.parquet`) after running `make pipeline` locally."
    )
