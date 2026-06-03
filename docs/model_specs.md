# Model Specs

## `stg_recruits`

- **Grain:** one row per recruit record in source.
- **Purpose:** normalize names/program keys and calculate `recruit_input_score`.
- **Key fields:** `player_key`, `program_key`, `class_year`, `star_rating`, `recruit_input_score`.

## `stg_nfl_draft`

- **Grain:** one row per drafted player record in source.
- **Purpose:** standardize draft fields and calculate `draft_outcome_score`.
- **Key fields:** `player_key`, `draft_year`, `draft_round`, `draft_pick_overall`, `draft_outcome_score`.

## `stg_player_bridge`

- **Grain:** one row per matched recruit-to-draft identity record.
- **Purpose:** preserve match diagnostics and optional override linking.
- **Key fields:** `player_key`, `program_key`, `class_year`, `match_confidence`, `match_rule`.

## `mart_player_outcomes`

- **Grain:** one row per recruit.
- **Purpose:** join recruits to draft results without scoring logic.
- **Key fields:** `draft_outcome_score`, `drafted_flag`, `recruit_input_score`.

## `mart_star_baselines`

- **Grain:** one row per `star_rating`.
- **Purpose:** national expected draft outcome and draft rate baselines.
- **Key fields:** `expected_outcome_score`, `expected_draft_rate`, `national_draft_conversion_rate`.

## `mart_player_development`

- **Grain:** one row per recruit.
- **Purpose:** compare draft outcomes to national star-level baseline.
- **Key fields:** `expected_outcome_score`, `player_development_score`, `beat_expectation_flag`.

## `mart_program_year`

- **Grain:** one row per `program_key` and `class_year`.
- **Purpose:** aggregate relative and absolute program-year metrics.
- **Key fields:** `program_development_index`, `total_value_added`, `positive_development_rate`, `draft_conversion_rate`.
