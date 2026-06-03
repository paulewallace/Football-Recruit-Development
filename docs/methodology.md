# Methodology

## Question

Which college football programs develop recruiting talent into NFL draft outcomes **better than expected** for the recruit profiles they sign?

## Data sources

| Dataset | Source |
|---|---|
| Recruiting classes (2012–2023) | [CollegeFootballData.com](https://collegefootballdata.com/) API |
| NFL draft picks (2016–2024) | [nflverse](https://github.com/nflverse/nflverse-data) via `nfl_data_py` |
| Program / conference reference | CFBD `/teams` endpoint |

## Pipeline

1. **Ingest** — pull raw data to Parquet (`make ingest`)
2. **Match** — link recruits to draft outcomes (`make match`)
3. **Transform** — build staging and mart tables in DuckDB (`make transform`)

## Matching rules

Recruits are linked to NFL draft records using:

1. **High confidence:** exact normalized `player_key` within a draft year window (class year + 3 to 6 years)
2. **Medium confidence:** fuzzy name match (≥92 similarity) within the same window
3. Unmatched recruits are exported to `data/staging/unmatched_recruits.parquet` for review

Each match includes `match_confidence` and `match_rule`.

## Scoring approach (v1)

Development is measured **relative to a national baseline**, not against raw star points.

1. Assign **`draft_outcome_score`** from draft result (0 if undrafted; round-weighted points if drafted)
2. Compute **`expected_outcome_score`** = national average draft outcome for the same star rating
3. **`player_development_score`** = `draft_outcome_score - expected_outcome_score`
4. Aggregate to program × class year metrics (average, total value added, positive rate)

See the **National baselines** tab for current expected values by star.

## Program metrics

- **`program_development_index`** — average player development score for the class
- **`total_value_added`** — sum of development scores (volume-adjusted impact)
- **`positive_development_rate`** — share of recruits beating their star baseline
- **`draft_conversion_rate`** — absolute drafted / recruits (shown for context)

## Known limitations

- **Transfer portal:** credit may go to the signing school, not the school where the player developed
- **Name matching:** common names can produce ambiguous joins
- **Coverage:** API completeness varies by season; recent classes have incomplete draft outcomes
- **Draft-only v1:** undrafted players who make NFL rosters are scored as 0 until v2 league data is added
- **Heuristic weights:** round weights and baselines should be sensitivity-tested over time

## Roadmap

- **v1 (current):** draft outcomes vs national star baselines
- **v2:** early NFL career outcomes (games, starts, value metrics)
- **v3 (optional):** transfer-aware attribution and position-level baselines
