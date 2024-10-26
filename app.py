# pylint: disable=missing-module-docstring
# https://srssql.streamlit.app/
import io

import duckdb
import pandas as pd
import streamlit as st

# PARTIE DATA
# ajout de vrai data pour les questions
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie, 2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_QUERY = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
answer_df = duckdb.sql(ANSWER_QUERY).df()

# PARTIE AFFICHAGE
# titre de la page
st.write(
    """
# SRS SQL 
Spaced Repetition System SQL practice
"""
)

# sidebar pour choisir le thème à réviser
with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ["Joins", "GroupBy", "Window Functions"],
        index=None,  # Default choice is None
        placeholder="Select what you want to review",
    )
    st.write("You selected:", option)

# ajout d'un header pour poser la question
st.header("enter your code:")
input_query = st.text_area(label="your SQL code here", key="user_input")
# key = user_input sert à nommer la clé du widget (pour le retrouver après)

# test si la query n'est pas vide
if input_query:
    input_df = duckdb.sql(input_query).df()
    st.dataframe(input_df)

    # il reste à faire : tester si la réponse = la solution
    # 1ere idée :
    if len(input_df.columns) != len(answer_df.columns):
        st.write("some columns are missing")

    nb_lines_difference = answer_df.shape[0] - input_df.shape[0]
    if nb_lines_difference != 0:
        st.write(f"there are {nb_lines_difference} lines missing")

# tabs présentant le contexte de l'exercice et la solution
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(answer_df)

with tab3:
    st.write(ANSWER_QUERY)
