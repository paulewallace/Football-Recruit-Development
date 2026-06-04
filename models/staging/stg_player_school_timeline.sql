create or replace table stg_player_school_timeline as
select
    lower(regexp_replace(trim(cast(player_key as varchar)), '[^a-zA-Z0-9]+', '', 'g')) as player_key,
    try_cast(class_year as integer) as class_year,
    lower(regexp_replace(trim(cast(signing_program_key as varchar)), '[^a-zA-Z0-9]+', ' ', 'g')) as signing_program_key,
    lower(regexp_replace(trim(cast(development_program_key as varchar)), '[^a-zA-Z0-9]+', ' ', 'g')) as development_program_key,
    try_cast(transfer_count as integer) as transfer_count,
    lower(trim(cast(attribution_rule as varchar))) as attribution_rule,
    coalesce(try_cast(is_transfer as boolean), false) as is_transfer
from read_parquet('data/staging/player_school_timeline.parquet');
