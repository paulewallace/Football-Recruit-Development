# Metrics Definitions

## Metric Philosophy

Evaluate player development by comparing **realized draft outcomes** to **national baseline outcomes** for the same recruit profile (star rating). Program rollups depend on which attribution view you select.

## Program attribution views

| Mart | Credits program by |
|---|---|
| `mart_program_year_signing` | HS signing school |
| `mart_program_year_development` | Last transfer portal destination |
| `mart_program_year` | View alias → signing (backward compatible) |

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

`expected_outcome_score = avg(draft_outcome_score)` by `star_rating` in `mart_star_baselines`.

## Player Development Score (primary)

`player_development_score = draft_outcome_score - expected_outcome_score`

Scores are **player-level**; the same score is attributed to signing or development school in separate program marts (never double-counted in one view).

## Program Metrics

| Metric | Definition |
|---|---|
| `program_development_index` | `avg(player_development_score)` per program × class year |
| `total_value_added` | `sum(player_development_score)` per program × class year |
| `positive_development_rate` | share with `player_development_score > 0` |
| `transfer_player_rate` | share with `is_transfer = true` |
| `draft_conversion_rate` | `drafted / recruits` (absolute) |

## League Success (v2, planned)

Add `league_success_score` to `total_outcome_score` once early-career NFL data is integrated.
