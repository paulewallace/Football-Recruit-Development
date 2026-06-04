# Data Pipeline

## Flow

```text
CFBD API ──► data/raw/recruits.parquet
nflverse ──► data/raw/nfl_draft.parquet
CFBD API ──► data/raw/programs.parquet
CFBD API ──► data/raw/transfers.parquet
                │
                ▼
    player_bridge.parquet + player_school_timeline.parquet
                │
                ▼
         warehouse/college_dev.duckdb
           ├── stg_* tables
           └── mart_* tables
```

## Commands

| Step | Command | Output |
|---|---|---|
| Ingest | `make ingest` | `data/raw/*.parquet` (includes transfers) |
| Match | `make match` | `player_bridge.parquet`, `player_school_timeline.parquet` |
| Transform | `make transform` | `warehouse/college_dev.duckdb` |

## School timeline rules

1. **Signing school** from recruit `committedTo`
2. **Development school** = last portal destination in draft window, else signing
3. `attribution_rule`: `no_transfer`, `last_destination`, or `unmatched_transfer`

## Matching rules (draft)

1. **High confidence:** exact normalized `player_key` within draft year window (class year + 3–6).
2. **Medium confidence:** fuzzy name match (≥92) within the same year window.
