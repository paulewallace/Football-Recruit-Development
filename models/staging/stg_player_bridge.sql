create or replace table stg_player_bridge as
with source as (
    select *
    from read_parquet('data/staging/player_bridge.parquet')
)
select
    lower(regexp_replace(trim(cast(player_key as varchar)), '[^a-zA-Z0-9]+', '', 'g')) as player_key,
    lower(trim(cast(recruit_player_name as varchar))) as recruit_player_name,
    lower(trim(cast(draft_player_name as varchar))) as draft_player_name,
    lower(regexp_replace(trim(cast(program_key as varchar)), '[^a-zA-Z0-9]+', ' ', 'g')) as program_key,
    try_cast(class_year as integer) as class_year,
    try_cast(draft_year as integer) as draft_year,
    lower(trim(cast(match_confidence as varchar))) as match_confidence,
    lower(trim(cast(match_rule as varchar))) as match_rule
from source;
