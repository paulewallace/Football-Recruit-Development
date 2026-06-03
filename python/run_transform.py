from pathlib import Path
import duckdb

from python.db import DB_PATH


def execute_sql_file(conn: duckdb.DuckDBPyConnection, sql_path: Path) -> None:
    sql = sql_path.read_text()
    conn.execute(sql)
    print(f"Ran {sql_path}")


def main() -> None:
    db_path = DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)

    staging_sql = sorted(Path("models/staging").glob("*.sql"))
    mart_sql = [
        Path("models/marts/mart_player_outcomes.sql"),
        Path("models/marts/mart_star_baselines.sql"),
        Path("models/marts/mart_player_development.sql"),
        Path("models/marts/mart_program_year.sql"),
    ]

    with duckdb.connect(str(db_path)) as conn:
        for sql_path in staging_sql + mart_sql:
            execute_sql_file(conn, sql_path)

        # Backward-compatible placeholder for app wiring while UI evolves.
        conn.execute(
            """
            create or replace view mart_star_uplift as
            select
                p.program_key,
                p.class_year,
                3 as star_rating,
                p.recruits,
                p.drafted_recruits as drafted,
                p.draft_conversion_rate as drafted_rate,
                b.national_draft_conversion_rate as national_drafted_rate,
                p.dev_score_3_star as uplift
            from mart_program_year p
            cross join (
                select national_draft_conversion_rate
                from mart_star_baselines
                where star_rating = 3
            ) b
            """
        )

    print(f"Transform complete in {db_path}")


if __name__ == "__main__":
    main()
