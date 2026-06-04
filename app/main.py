import sys
from pathlib import Path

# Streamlit Cloud runs app/main.py with cwd=sys.path[0]=app/, so `python` package is not found.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.bootstrap import ensure_warehouse, setup_path, warehouse_status_message

setup_path()

import streamlit as st

from python.db import PROJECT_ROOT, query

ensure_warehouse()

DOCS_DIR = PROJECT_ROOT / "docs"

_missing_warehouse_msg = warehouse_status_message()


def load_doc(filename: str) -> str:
    path = DOCS_DIR / filename
    if not path.exists():
        return f"*{filename} not found.*"
    return path.read_text(encoding="utf-8")


st.set_page_config(page_title="CFB -> NFL Development", layout="wide")

st.title("College Program NFL Development")
st.caption(
    "Development = draft outcome vs national baseline for the same star rating. "
    "Absolute draft rate shown for context."
)

if _missing_warehouse_msg:
    st.error(_missing_warehouse_msg)
    st.stop()

tab_leaderboard, tab_baselines, tab_methodology = st.tabs(
    ["Leaderboard", "National baselines", "Methodology"]
)


PROGRAM_YEAR_TABLES = {
    "Signing school (HS commit)": "mart_program_year_signing",
    "Development school (last portal destination)": "mart_program_year_development",
}


@st.cache_data
def load_program_year(
    min_recruits: int,
    recruiting_years: tuple[int, ...],
    table_name: str,
):
    sql = f"""
        SELECT
            program_key,
            class_year,
            recruits,
            drafted_recruits,
            draft_conversion_rate,
            program_development_index,
            total_value_added,
            positive_development_rate,
            transfer_player_rate,
            avg_draft_outcome_score,
            avg_expected_outcome_score,
            outcome_vs_expected_gap
        FROM {table_name}
        WHERE recruits >= $min_recruits
    """
    params: dict = {"min_recruits": min_recruits}
    if recruiting_years:
        sql += " AND class_year IN (SELECT UNNEST($recruiting_years))"
        params["recruiting_years"] = list(recruiting_years)
    sql += " ORDER BY program_development_index DESC"
    return query(sql, params)


@st.cache_data
def load_baselines():
    return query("""
        SELECT
            star_rating,
            national_recruits,
            expected_outcome_score,
            national_draft_conversion_rate
        FROM mart_star_baselines
        ORDER BY star_rating DESC
    """)


with tab_leaderboard:
    st.subheader("Program development leaderboard")
    attribution_label = st.radio(
        "Credit development to",
        options=list(PROGRAM_YEAR_TABLES.keys()),
        horizontal=True,
    )
    table_name = PROGRAM_YEAR_TABLES[attribution_label]
    st.markdown(
        "**Relative:** `program_development_index` (avg outcome vs national baseline by star).  \n"
        "**Absolute:** `draft_conversion_rate`, `avg_draft_outcome_score`.  \n"
        "**Signing** = HS commit school · **Development** = last transfer destination (portal era)."
    )
    recruiting_year = st.multiselect(
        "Recruiting year (empty = all years)",
        options=list(range(2012, 2024)),
    )
    min_recruits = st.slider("Minimum recruits per class year", 1, 25, 5)
    try:
        df = load_program_year(min_recruits, tuple(recruiting_year), table_name)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"{len(df):,} program-class rows")
    except FileNotFoundError as exc:
        st.error(str(exc))

with tab_baselines:
    st.subheader("National star baselines")
    st.markdown(
        "Expected outcomes used in development scoring. "
        "A 3-star who goes undrafted scores near **0** if the national 3-star baseline is also near 0."
    )
    try:
        st.dataframe(load_baselines(), use_container_width=True, hide_index=True)
    except FileNotFoundError as exc:
        st.error(str(exc))

with tab_methodology:
    st.subheader("How this works")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            **Core formula**

            `player_development_score = draft_outcome_score − expected_outcome_score`

            `expected_outcome_score` is the national average draft outcome for that **star rating**.

            **Interpretation**
            - Positive → beat the national baseline for that recruit profile
            - Near zero → typical outcome for that star level
            - Negative → below national baseline
            """
        )
    with col2:
        st.markdown(
            """
            **Draft outcome points (v1)**

            | Result | Points |
            |---|---|
            | Undrafted | 0 |
            | Rd 7 | 10 |
            | Rd 6 | 20 |
            | Rd 5 | 30 |
            | Rd 4 | 45 |
            | Rd 3 | 60 |
            | Rd 2 | 80 |
            | Rd 1 | 100 |
            """
        )

    st.divider()

    with st.expander("Full methodology", expanded=True):
        st.markdown(load_doc("methodology.md"))

    with st.expander("Metric definitions"):
        st.markdown(load_doc("metrics.md"))

    st.divider()
    st.caption(
        "Recruiting: CollegeFootballData.com · Draft: nflverse · "
        "Pipeline rebuild: `make pipeline`"
    )
