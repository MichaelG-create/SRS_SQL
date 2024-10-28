# pylint: disable=missing-module-docstring
# https://srssql.streamlit.app/
# https://srssql-develop.streamlit.app/

import os
import logging  # logger de python
from ast import Index

from streamlit.logger import get_logger # logger de streamlit

import duckdb
import streamlit as st

# checking streamlit cloud configuration
app_logger = get_logger(__name__)
app_logger.setLevel(logging.INFO)  # here can set DEBUG, ERROR, WARNING

if "data" not in os.listdir():
    app_logger.info("duckdb database set up")
    app_logger.info("List working directory content: %s", os.listdir())
    app_logger.info("Create 'data' folder, if it doesn't exist")
    os.makedirs("data", exist_ok=True)  # exist_ok useful if "if" not used

if "sql_exercises.duckdb" not in os.listdir("data"):
    app_logger.info("Create Database and tables")
    subprocess.run([f"{sys.executable}", "SRS_SQL/init_db.py"], check=False)

# connecting db
con = duckdb.connect(database="data/sql_exercises.duckdb", read_only=False)

# ------------------------------------------------------------------------
# DISPLAY PART
# ------------------------------------------------------------------------
# Page title
st.write(
    """
# SRS SQL 
Spaced Repetition System SQL practice
"""
)

# -----------------------------------------------------------
# Sidebar to choose the theme to revise
# -----------------------------------------------------------
with (st.sidebar):
    theme_selected = st.selectbox(
        "What would you like to review?",
        ["cross_joins", "GroupBy", "simple_window"],
        index=None,  # Default choice is None
        placeholder="Select what you want to review",
    )
    # theme selected
    try:
        st.write("You selected:", theme_selected)

        # get available exercises in this theme
        # sort the exercises by last_reviewed
        exercise = con.execute(
            f"SELECT DISTINCT * FROM memory_state WHERE theme = '{theme_selected}'"
        ).df().sort_values("last_reviewed", ascending=True)
        st.write(exercise)

        # load answer of the 1st exercise (for instance)
        exercise_name = exercise.iloc[0]["exercise_name"]

        # get answer_query stored in the exercise solution file
        with open(
            f"answers/{exercise_name}.sql", "r", encoding="utf-8"
        ) as f:  # r for read only
            answer_query = f.read()

        # load solution df using answer_query
        solution_df = con.execute(answer_query).df()

    # no theme selected
    except IndexError as e:     #KeyError if use .loc instead of .iloc
        st.write("")

# -----------------------------------------------------------
# Input zone
# -----------------------------------------------------------
# Question header
st.header("enter your code:")
input_query = st.text_area(label="your SQL code here", key="user_input")
# key names the widget (to get it back later)

# -----------------------------------------------------------
# Input reaction zone
# -----------------------------------------------------------
# input_query sent
try:
    # Remark : user can query any table of db without choosing a theme !
    input_df = con.execute(input_query).df()
    st.dataframe(input_df)

    # theme chosen
    try:
        # give a hint on lines difference
        nb_lines_difference = solution_df.shape[0] - input_df.shape[0]
        if nb_lines_difference != 0:
            if nb_lines_difference > 0:
                st.write(f"The solution has {nb_lines_difference} lines more.")
            else:
                st.write(f"The solution has {-nb_lines_difference} lines less.")

        # sort solution_df columns like input_df's to ease comparison
        try:
            input_df = input_df[solution_df.columns]
            # compare
            try:
                comparison_result = input_df.compare(solution_df)
                # No difference found
                if comparison_result.empty:
                    st.write("You found the right solution.")
                else:
                    st.write("Not yet, here are the differences :")
                    st.dataframe(comparison_result)
            # value error
            except ValueError as e:
                st.write(f"{e}")
        # different columns
        except KeyError:
            st.write("Some columns are missing or different.")
    # no theme : no solution
    except NameError as e:
        st.write("No theme selected yet, no solution loaded.")
        # st.write(f"{e}")

# no input_query
except AttributeError as e:
    st.write("")
    # st.write("No input sent yet.")
# input_query : syntax error (duckdb)
except duckdb.duckdb.ParserException as e:
    st.write("incorrect input sent, not an SQL command")
    st.write(f"{e}")
# input_query : missing table (duckdb)
except duckdb.duckdb.CatalogException as e:
    st.write(f"{e}")


# -----------------------------------------------------------
# tabs with exercise specifics and solution
# -----------------------------------------------------------
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    # show exercise tables
    # use df.loc[0,"tables"] : get 1st line in "tables" column
    # tables : names of the tables of an exercise
    # theme chosen
    # if theme_selected:
    try:
        exercise_tables = exercise.iloc[0]["tables"]
        for table in exercise_tables:
            # load tables
            st.write(f"table: {table}")
            df_table = con.execute(f'SELECT * FROM "{table}"').df()
            st.dataframe(df_table)

        #load solution_df
        st.write("expected:")
        st.dataframe(solution_df)
    # no theme : no solution
    except IndexError as e:     #KeyError if use .loc instead of .iloc
        st.write("")
        # st.write("No exercise selected yet, no tables loaded.")

with tab3:
    if theme_selected:
        st.write(answer_query)
        # bad formatting for now
