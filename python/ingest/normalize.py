"""Name and key normalization for matching."""
import re

import pandas as pd


def normalize_name(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def player_key(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", normalize_name(value))
