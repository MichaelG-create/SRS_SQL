# pylint: disable=missing-module-docstring
import logging
import os

import streamlit as st
from streamlit.logger import get_logger

from srs_sql.db import get_connection, init_base_tables, init_exercises
from srs_sql.models import Exercise


# ------------------------------------------------------------------------
# Logging / setup
# ------------------------------------------------------------------------
app_logger = get_logger(__name__)
app_logger.setLevel(logging.INFO)

if "data" not in os.listdir():
    app_logger.info("Create 'data' folder")
    os.makedirs("data", exist_ok=True)

# ------------------------------------------------------------------------
# DB init
# ------------------------------------------------------------------------
con = get_connection()
init_base_tables(con)
init_exercises(con)

# ------------------------------------------------------------------------
# Exercise object
# ------------------------------------------------------------------------
exercise = Exercise(con)

# ------------------------------------------------------------------------
# Page title
# ------------------------------------------------------------------------
st.write(
    """
# SRS SQL
Spaced Repetition System SQL practice
"""
)

# ------------------------------------------------------------------------
# Sidebar: ONLY selection controls (no tables, no solutions)
# ------------------------------------------------------------------------
with st.sidebar:
    # 1) Choose review mode FIRST
    review_mode = st.radio(
        "Review mode",
        ["By last review date", "By difficulty"],
        key="review_mode",
    )

    theme_selected = None

    if review_mode == "By difficulty":
        # Only then show the theme selector
        themes_df = con.execute(
            """
            SELECT theme, MIN(difficulty) AS min_diff
            FROM exercises
            GROUP BY theme
            ORDER BY min_diff ASC, theme ASC
            """
        ).df()
        theme_list = themes_df["theme"].tolist()

        theme_selected = st.selectbox(
            "What would you like to review?",
            theme_list,
            index=None,
            placeholder="Select what you want to review",
            key="theme_select",
        )

# ------------------------------------------------------------------------
# Exercise brief and input area (main area)
# ------------------------------------------------------------------------
# Main central area: Load + ALL exercise content
exercise = Exercise(con)  # Or use session_state if needed for persistence
exercise.load_from_theme(theme_selected, review_mode=review_mode)

# If nothing loaded (e.g. no exercises), stop
if not exercise.name:
    st.write("No exercise available.")
    st.stop()

if exercise.instruction:
    st.subheader("Exercise brief")
    st.write(exercise.instruction)

# Tabs for tables / solution (main area)
tab1, tab2 = st.tabs(["Tables", "Solution"])
with tab1:
    # col1, col2 = st.columns(2)
    # with col1:
    exercise.show_tables()
    # with col2:
    exercise.show_expected()
with tab2:
    exercise.show_solution()

st.header("Enter your code:")
input_query = st.text_area(label="Your SQL code here")

exercise.check_user_solution(input_query)


# ------------------------------------------------------------------------
# SRS buttons (main area)
# ------------------------------------------------------------------------
exercise.srs_buttons()
