-- Backward-compatible alias: signing school attribution (HS commit).
-- Drop view before table: DuckDB errors if you DROP TABLE on an existing view.
drop view if exists mart_program_year;
drop table if exists mart_program_year;
create view mart_program_year as
select * exclude (attribution_type)
from mart_program_year_signing;
