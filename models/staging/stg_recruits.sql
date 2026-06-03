create or replace table stg_recruits as
with source as (
    select *
    from read_parquet('data/raw/recruits.parquet')
)
select
    lower(trim(cast(player_name as varchar))) as recruit_player_name,
    lower(regexp_replace(trim(cast(player_name as varchar)), '[^a-zA-Z0-9]+', ' ', 'g')) as recruit_player_name_norm,
    trim(cast(program as varchar)) as program,
    lower(regexp_replace(trim(cast(program as varchar)), '[^a-zA-Z0-9]+', ' ', 'g')) as program_key,
    try_cast(class_year as integer) as class_year,
    try_cast(star_rating as integer) as star_rating,
    trim(cast(position as varchar)) as position,
    case
        when try_cast(star_rating as integer) >= 5 then 100
        when try_cast(star_rating as integer) = 4 then 75
        when try_cast(star_rating as integer) = 3 then 45
        when try_cast(star_rating as integer) = 2 then 20
        else 10
    end as recruit_input_score,
    lower(regexp_replace(trim(cast(player_name as varchar)), '[^a-zA-Z0-9]+', '', 'g')) as player_key
from source;
