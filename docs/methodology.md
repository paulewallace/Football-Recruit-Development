# Methodology

## Question

Which college football programs develop recruiting talent into NFL draft outcomes **better than expected** for the recruit profiles they sign?

## Data sources

| Dataset | Source |
|---|---|
| Recruiting classes (2012–2023) | [CollegeFootballData.com](https://collegefootballdata.com/) API |
| NFL draft picks (2016–2024) | [nflverse](https://github.com/nflverse/nflverse-data) via `nfl_data_py` |
| Transfer portal (2018–2024) | CFBD `/player/portal` |
| Program / conference reference | CFBD `/teams` endpoint |

## Pipeline

1. **Ingest** — pull raw data to Parquet (`make ingest`)
2. **Match** — link recruits to draft outcomes and build school timeline (`make match`)
3. **Transform** — build staging and mart tables in DuckDB (`make transform`)

## Dual program attribution

Program credit is shown two ways:

| View | Definition |
|---|---|
| **Signing school** | HS commit (`committedTo`) — where the recruit originally signed |
| **Development school** | Last transfer portal **destination** before the NFL draft window; if no portal match, same as signing |

`is_transfer` flags recruits where signing and development schools differ.

**MVP limitation:** development school uses last portal destination, not seasons on roster. Future v2 may use CFBD roster data for tenure-based credit.

## Matching rules

**Recruit → NFL draft**

1. **High confidence:** exact normalized `player_key` within a draft year window (class year + 3 to 6 years)
2. **Medium confidence:** fuzzy name match (≥92 similarity) within the same window

**Recruit → transfer portal**

1. Match portal entries to recruits by `player_key` or fuzzy name within the draft window
2. Latest portal season determines development school

## Scoring approach (v1)

Development is measured **relative to a national baseline**, not against raw star points.

1. Assign **`draft_outcome_score`** from draft result (0 if undrafted; round-weighted points if drafted)
2. Compute **`expected_outcome_score`** = national average draft outcome for the same star rating
3. **`player_development_score`** = `draft_outcome_score - expected_outcome_score`
4. Aggregate to program × class year metrics by signing or development school

## Program metrics

- **`program_development_index`** — average player development score for the class
- **`total_value_added`** — sum of development scores (volume-adjusted impact)
- **`positive_development_rate`** — share of recruits beating their star baseline
- **`transfer_player_rate`** — share of recruits with signing ≠ development school
- **`draft_conversion_rate`** — absolute drafted / recruits (shown for context)

## Known limitations

- **Last destination proxy:** may not reflect where most development occurred
- **Pre-2018 classes:** little portal data; development school usually equals signing school
- **Name matching:** common names can produce ambiguous joins
- **Coverage:** API completeness varies by season; recent classes have incomplete draft outcomes
- **Draft-only v1:** undrafted players who make NFL rosters are scored as 0 until v2 league data is added

## Roadmap

- **v1 (current):** draft outcomes vs national star baselines + dual attribution
- **v2:** early NFL career outcomes (games, starts, value metrics)
- **v3:** roster-tenure attribution when portal data is incomplete
