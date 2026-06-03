create or replace table stg_nfl_draft as
with source as (
    select *
    from read_parquet('data/raw/nfl_draft.parquet')
)
select
    lower(trim(cast(player_name as varchar))) as draft_player_name,
    lower(regexp_replace(trim(cast(player_name as varchar)), '[^a-zA-Z0-9]+', ' ', 'g')) as draft_player_name_norm,
    try_cast(draft_year as integer) as draft_year,
    try_cast(draft_round as integer) as draft_round,
    try_cast(draft_pick_overall as integer) as draft_pick_overall,
    trim(cast(nfl_team as varchar)) as nfl_team,
    case
        when try_cast(draft_round as integer) = 1 then 100
        when try_cast(draft_round as integer) = 2 then 80
        when try_cast(draft_round as integer) = 3 then 60
        when try_cast(draft_round as integer) = 4 then 45
        when try_cast(draft_round as integer) = 5 then 30
        when try_cast(draft_round as integer) = 6 then 20
        when try_cast(draft_round as integer) = 7 then 10
        else 0
    end as draft_outcome_score,
    lower(regexp_replace(trim(cast(player_name as varchar)), '[^a-zA-Z0-9]+', '', 'g')) as player_key
from source;
