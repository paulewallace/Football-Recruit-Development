create or replace table mart_player_outcomes as
with recruits as (
    select *
    from stg_recruits
),
bridge as (
    select *
    from stg_player_bridge
),
draft as (
    select *
    from stg_nfl_draft
)
select
    r.player_key,
    coalesce(b.program_key, r.program_key) as program_key,
    coalesce(b.class_year, r.class_year) as class_year,
    r.recruit_player_name,
    r.position,
    r.star_rating,
    r.recruit_input_score,
    d.draft_year,
    d.draft_round,
    d.draft_pick_overall,
    coalesce(d.draft_outcome_score, 0) as draft_outcome_score,
    coalesce(d.draft_outcome_score, 0) as total_outcome_score,
    case when d.player_key is null then 0 else 1 end as drafted_flag,
    coalesce(b.match_confidence, 'none') as match_confidence,
    coalesce(b.match_rule, 'direct_player_key') as match_rule
from recruits r
left join bridge b
    on r.player_key = b.player_key
    and r.class_year = b.class_year
left join draft d
    on coalesce(b.player_key, r.player_key) = d.player_key;
