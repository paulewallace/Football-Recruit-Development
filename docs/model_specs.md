# Model Specs

## `stg_recruits`

- **Grain:** one row per recruit record in source.
- **Purpose:** normalize names/program keys and calculate `recruit_input_score`.
- **Key fields:** `player_key`, `program_key`, `class_year`, `star_rating`, `recruit_input_score`.

## `stg_nfl_draft`

- **Grain:** one row per drafted player record in source.
- **Purpose:** standardize draft fields and calculate `draft_outcome_score`.

## `stg_player_bridge`

- **Grain:** one row per matched recruit-to-draft identity record.

## `stg_player_school_timeline`

- **Grain:** one row per `player_key` + `class_year`.
- **Purpose:** signing vs development program attribution.
- **Key fields:** `signing_program_key`, `development_program_key`, `is_transfer`, `attribution_rule`.

## `mart_player_outcomes`

- **Grain:** one row per recruit.
- **Key fields:** `signing_program_key`, `development_program_key`, `program_key` (alias of signing), `draft_outcome_score`, `is_transfer`.

## `mart_player_development`

- **Grain:** one row per recruit.
- **Key fields:** `player_development_score`, both program keys, `is_transfer`.

## `mart_program_year_signing`

- **Grain:** one row per signing `program_key` and `class_year`.
- **Purpose:** program metrics credited to HS commit school.

## `mart_program_year_development`

- **Grain:** one row per development `program_key` and `class_year`.
- **Purpose:** program metrics credited to last portal destination.

## `mart_program_year`

- **Type:** view over `mart_program_year_signing` (backward compatible).
