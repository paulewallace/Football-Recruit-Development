# Data Pipeline

## Flow

```text
CFBD API ──► data/raw/recruits.parquet
nflverse ──► data/raw/nfl_draft.parquet
CFBD API ──► data/raw/programs.parquet
                │
                ▼
         player_bridge.parquet (matching)
                │
                ▼
         warehouse/college_dev.duckdb
           ├── stg_* tables
           └── mart_* tables
```

## Commands

| Step | Command | Output |
|---|---|---|
| Ingest | `make ingest` | `data/raw/*.parquet` |
| Match | `make match` | `data/staging/player_bridge.parquet` |
| Transform | `make transform` | `warehouse/college_dev.duckdb` |

## Matching rules

1. **High confidence:** exact normalized `player_key` within draft year window (class year + 3–6).
2. **Medium confidence:** fuzzy name match (≥92) within the same year window.
3. Unmatched recruits are written to `data/staging/unmatched_recruits.parquet` for review.
