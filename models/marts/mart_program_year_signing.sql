create or replace table mart_program_year_signing as
with base as (
    select *
    from mart_player_development
),
aggregated as (
    select
        signing_program_key as program_key,
        class_year,
        count(*) as recruits,
        sum(drafted_flag) as drafted_recruits,
        round(avg(recruit_input_score), 2) as avg_recruit_input_score,
        round(avg(draft_outcome_score), 2) as avg_draft_outcome_score,
        round(avg(expected_outcome_score), 2) as avg_expected_outcome_score,
        round(avg(total_outcome_score), 2) as avg_total_outcome_score,
        round(avg(player_development_score), 4) as program_development_index,
        round(sum(player_development_score), 2) as total_value_added,
        round(avg(beat_expectation_flag::double), 4) as positive_development_rate,
        round(avg(is_transfer::double), 4) as transfer_player_rate,
        round(avg(case when star_rating = 5 then player_development_score end), 4) as dev_score_5_star,
        round(avg(case when star_rating = 4 then player_development_score end), 4) as dev_score_4_star,
        round(avg(case when star_rating = 3 then player_development_score end), 4) as dev_score_3_star,
        round(avg(case when star_rating = 2 then player_development_score end), 4) as dev_score_2_star
    from base
    group by 1, 2
)
select
    *,
    'signing' as attribution_type,
    case
        when recruits = 0 then 0
        else round(drafted_recruits::double / recruits, 4)
    end as draft_conversion_rate,
    round(avg_total_outcome_score - avg_expected_outcome_score, 4) as outcome_vs_expected_gap
from aggregated;
