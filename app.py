# pylint: disable=missing-module-docstring
# https://srssql.streamlit.app/


import duckdb
import streamlit as st



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
        ["cross_joins", "GroupBy", "Window Functions"],
        index=None,  # Default choice is None
        placeholder="Select what you want to review",
    )
    st.write("You selected:", option)

# ajout d'un header pour poser la question
st.header("enter your code:")
input_query = st.text_area(label="your SQL code here", key="user_input")
# key = user_input sert à nommer la clé du widget (pour le retrouver après)

# test si la query n'est pas vide
# if input_query:
#     input_df = duckdb.sql(input_query).df()
#     st.dataframe(input_df)
#
#     nb_lines_difference = answer_df.shape[0] - input_df.shape[0]
#     if nb_lines_difference != 0:
#         st.write(f"there are {nb_lines_difference} lines missing")
#
#     # il reste à faire : tester si la réponse = la solution
#     # 1ere idée : comparaison de tailles (colonnes puis lignes)
#     if len(input_df.columns) != len(answer_df.columns):
#         st.write("some columns are missing")
#
#     # on choisit de mettre les colonnes de l'answer_df dans le même ordre que celles de l'input_df
#     # pour faciliter la comparaison après
#     try:
#         input_df = input_df[answer_df.columns]
#     # bug si pas les mêmes colonnes
#     except KeyError:
#         st.write("some columns are missing")
#
#     # Après un tour dans la doc pandas
#     # nécessite que les noms de colonnes soient identiques
#     # affiche le dataframe de comparaison des dataframes input et answer
#     # probleme : si tailles des df différentes :
#     # ValueError: Can only compare identically-labeled (both index and columns) DataFrame objects
#     try:
#         st.dataframe(input_df.compare(answer_df))
#     # si ça bug sur une value error, on affiche juste son message
#     except ValueError as e:
#         st.write(f"{e}")
#
#
# # tabs présentant le contexte de l'exercice et la solution
# tab2, tab3 = st.tabs(["Tables", "Solution"])
#
# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(answer_df)
#
# with tab3:
#     st.write(ANSWER_QUERY)
