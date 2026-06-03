create or replace table mart_star_baselines as
select
    star_rating,
    count(*) as national_recruits,
    round(avg(draft_outcome_score), 4) as expected_outcome_score,
    round(avg(drafted_flag::double), 4) as expected_draft_rate,
    round(sum(drafted_flag)::double / nullif(count(*), 0), 4) as national_draft_conversion_rate
from mart_player_outcomes
where star_rating is not null
group by 1;
