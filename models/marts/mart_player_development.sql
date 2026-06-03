create or replace table mart_player_development as
select
    o.player_key,
    o.program_key,
    o.class_year,
    o.recruit_player_name,
    o.position,
    o.star_rating,
    o.recruit_input_score,
    o.draft_year,
    o.draft_round,
    o.draft_pick_overall,
    o.draft_outcome_score,
    o.total_outcome_score,
    b.expected_outcome_score,
    b.expected_draft_rate,
    round(o.draft_outcome_score - b.expected_outcome_score, 4) as player_development_score,
    o.drafted_flag,
    case
        when o.draft_outcome_score > b.expected_outcome_score then 1
        else 0
    end as beat_expectation_flag,
    o.match_confidence,
    o.match_rule
from mart_player_outcomes o
left join mart_star_baselines b
    on o.star_rating = b.star_rating;
