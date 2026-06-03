# Metrics Definitions

## Metric Philosophy

Evaluate player development by comparing **realized draft outcomes** to **national baseline outcomes** for the same recruit profile (star rating). This avoids penalizing programs because most recruits are not drafted.

## Recruit Input Score (reference only)

Legacy intake scale kept for context; **not used** for the primary development metric.

| Stars | Score |
|---|---|
| 5-star | 100 |
| 4-star | 75 |
| 3-star | 45 |
| 2-star | 20 |

## Draft Outcome Score (v1)

| Result | Score |
|---|---|
| Undrafted | 0 |
| Round 7 | 10 |
| Round 6 | 20 |
| Round 5 | 30 |
| Round 4 | 45 |
| Round 3 | 60 |
| Round 2 | 80 |
| Round 1 | 100 |

## Expected Outcome Score (national baseline)

For each `star_rating`, computed across all recruits in the dataset:

`expected_outcome_score = avg(draft_outcome_score)` by star

`expected_draft_rate = avg(drafted_flag)` by star

Stored in `mart_star_baselines`.

## Player Development Score (primary)

`player_development_score = draft_outcome_score - expected_outcome_score`

- **Positive** → beat national baseline for that star level
- **Negative** → below national baseline for that star level
- Undrafted 3-star near **0** if national 3-star expected outcome is ~0

## Program Metrics

| Metric | Definition |
|---|---|
| `program_development_index` | `avg(player_development_score)` per program × class year |
| `total_value_added` | `sum(player_development_score)` per program × class year |
| `positive_development_rate` | share of recruits with `player_development_score > 0` |
| `draft_conversion_rate` | `drafted / recruits` (absolute) |
| `avg_draft_outcome_score` | mean draft points (absolute) |
| `outcome_vs_expected_gap` | `avg_draft_outcome - avg_expected_outcome` for the class |

## League Success (v2, planned)

Add `league_success_score` to `total_outcome_score` once early-career NFL data is integrated.
