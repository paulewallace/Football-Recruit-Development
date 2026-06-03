# Football Recruit Development

Streamlit portfolio project analyzing how college football programs develop recruiting talent into NFL and pro-level outcomes.

## MVP Scope

- Time window: `2012-2023`
- Population: all recruits (2-star through 5-star)
- Outcome definition (v1): NFL draft outcomes
- Outcome definition (v2): early NFL career outcomes
- Primary focus: development over expectation relative to incoming recruit profile
- Local-first stack: Python, DuckDB, Parquet, Streamlit

## Metric Framework

The app will use a phased scoring framework:

1. **Input Score (Recruit Profile)**
   - Baseline expected value based on recruit ranking/stars and position.
2. **Outcome Score (Draft)**
   - Outcome value based on whether drafted and draft position.
3. **Outcome Score (League Success, v2)**
   - Additional value from early NFL career signals (for example games played, starts, and approximate value style measures when available).
4. **Development Score**
   - `Outcome Score - Input Score`, aggregated to program/year and program-level trends.

This enables fair comparisons across programs with very different recruiting classes.

## Planned Project Structure

- `app/` Streamlit app code
- `python/ingest/` source ingestion scripts
- `python/matching/` recruit-to-draft identity matching scripts
- `models/staging/` cleaned standardized SQL models
- `models/marts/` analytical models for the app
- `docs/` metric and methodology documentation
- `data/raw/` source snapshots
- `data/staging/` intermediate datasets and bridge tables
- `warehouse/` DuckDB database file

## Data Sources

| Dataset | Source | Auth |
|---|---|---|
| Recruiting classes | [CollegeFootballData.com](https://collegefootballdata.com/) API | Free API key |
| NFL draft picks | [nflverse](https://github.com/nflverse/nflverse-data) via `nfl_data_py` | None |
| Program / conference | CFBD `/teams` endpoint | Same API key |

## Local Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Create `.env` (run this line by itself — do not paste comments after it):
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and paste your API key in quotes, e.g. `COLLEGE_FOOTBALL_DATA_API_KEY="your_key"`.
3. Run the pipeline:
   ```bash
   make ingest    # recruits + draft + programs
   make match     # recruit ↔ draft identity bridge
   make transform # DuckDB staging + marts
   make app       # Streamlit UI
   ```

Or run everything at once: `make pipeline`

## Streamlit Cloud deploy

Streamlit runs `app/main.py` with the repo root **not** on Python's module path by default, so the app adds the project root to `sys.path` before `from python.db import ...`.

**Required for Cloud:** the DuckDB warehouse must be in the repo. After running the pipeline locally:

```bash
make pipeline
git add -f warehouse/college_dev.duckdb
git commit -m "Add warehouse for Streamlit Cloud"
git push
```

Main module: `app/main.py` (set in Streamlit Cloud app settings).

Optional: commit `data/raw/*.parquet` too if you want Cloud to rebuild the warehouse on startup when the DB is missing.

## Notes

This repository is intentionally local-first and low-cost. It is structured to mirror analytics engineering best practices while staying free to run.
