"""Minimal CollegeFootballData.com API client."""
import time
from typing import Any, Optional

import pandas as pd
import requests

from python.ingest.config import CFBD_BASE_URL, get_cfbd_api_key


def _headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {get_cfbd_api_key()}"}


def get_json(path: str, params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
    url = f"{CFBD_BASE_URL}{path}"
    response = requests.get(url, headers=_headers(), params=params or {}, timeout=60)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise ValueError(f"Expected list from {path}, got {type(data)}")
    time.sleep(0.35)
    return data


def fetch_recruits(year: int) -> pd.DataFrame:
    rows = get_json(
        "/recruiting/players",
        {"year": year, "classification": "HighSchool"},
    )
    if not rows:
        return pd.DataFrame(
            columns=[
                "player_name",
                "program",
                "class_year",
                "star_rating",
                "position",
                "national_rank",
                "rating",
            ]
        )

    df = pd.DataFrame(rows)
    out = pd.DataFrame(
        {
            "player_name": df.get("name", pd.Series(dtype="string")).astype("string"),
            "program": df.get("committedTo", pd.Series(dtype="string")).astype("string"),
            "class_year": pd.to_numeric(df.get("year"), errors="coerce").astype("Int64"),
            "star_rating": pd.to_numeric(df.get("stars"), errors="coerce").astype("Int64"),
            "position": df.get("position", pd.Series(dtype="string")).astype("string"),
            "national_rank": pd.to_numeric(df.get("ranking"), errors="coerce").astype("Int64"),
            "rating": pd.to_numeric(df.get("rating"), errors="coerce"),
        }
    )
    out = out.dropna(subset=["player_name", "class_year"])
    out = out[out["program"].notna() & (out["program"].str.len() > 0)]
    return out
