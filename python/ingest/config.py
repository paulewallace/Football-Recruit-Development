"""Shared ingest configuration."""
from pathlib import Path
import os

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
RAW_DIR = PROJECT_ROOT / "data" / "raw"
STAGING_DIR = PROJECT_ROOT / "data" / "staging"

# Recruiting classes included in MVP (players who could draft ~2016–2027).
CLASS_YEAR_START = 2012
CLASS_YEAR_END = 2023

# NFL draft seasons to pull (covers early departures + standard 3–4 year paths).
DRAFT_YEAR_START = 2016
DRAFT_YEAR_END = 2024

CFBD_BASE_URL = "https://api.collegefootballdata.com"
CFBD_API_KEY_ENV = "COLLEGE_FOOTBALL_DATA_API_KEY"


def get_cfbd_api_key() -> str:
    key = os.environ.get(CFBD_API_KEY_ENV, "").strip()
    if not key:
        raise RuntimeError(
            f"Missing {CFBD_API_KEY_ENV}. "
            "Run: cp .env.example .env — then set your key in .env (use quotes around the value)."
        )
    return key
