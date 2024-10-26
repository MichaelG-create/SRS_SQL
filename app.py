# pylint: disable=missing-module-docstring
# https://srssql.streamlit.app/
import ast

import duckdb
import streamlit as st

# connexion à la db des exercices
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------------------
# PARTIE AFFICHAGE
# ------------------------------------------------------------------------
# titre de la page
st.write(
    """
# SRS SQL 
Spaced Repetition System SQL practice
"""
)

# -----------------------------------------------------------
# sidebar pour choisir le thème à réviser
# -----------------------------------------------------------
with st.sidebar:
    # à mettre ici : récupération de la liste des themes à partir d'un
    # SELECT DISTINCT dans la table memory_state
    theme_selected = st.selectbox(
        "What would you like to review?",
        ["cross_joins", "GroupBy", "simple_window"],
        index=None,  # Default choice is None
        placeholder="Select what you want to review",
    )
    st.write("You selected:", theme_selected)

    # récupération des exercices disponibles dans le thème choisi
    if theme_selected:
        exercise = con.execute(
            f"SELECT DISTINCT * FROM memory_state WHERE theme = '{theme_selected}'"
        ).df()
        # affichage de memory_table avec juste les lignes du thème choisis
        st.write(exercise)

        # chargement de la table solution du 1er exercice (pas choisi pour l'instant)
        solution_table_name = exercise.loc[0, "solution_table"]
        # solution_table_name = ast.literal_eval(exercise.loc[0, "solution_table"])
        st.write(f"solution table name: {solution_table_name}")
        # on va chercher la table en SQL avec son nom : easy
        solution_df = con.execute(f'SELECT * FROM "{solution_table_name}"').df()

        # # ajoute un autre sélecteur pour choisir l'exercice dans la liste
        # exercise_selected = st.selectbox(
        #     "Which exercise would you like to review?",
        #     exercise,
        #     index=None,  # Default choice is None
        #     placeholder="Select what you want to review",
        # )
        # st.write("You selected:", exercise_selected)

# -----------------------------------------------------------
# Zone d'input avec affichage du résultat de l'input
# -----------------------------------------------------------
# ajout d'un header pour poser la question
st.header("enter your code:")
input_query = st.text_area(label="your SQL code here", key="user_input")
# key = user_input sert à nommer la clé du widget (pour le retrouver après)

# -----------------------------------------------------------
# zone de réaction à l'input
# -----------------------------------------------------------
# test si la query n'est pas vide
if input_query:
    # input_df = duckdb.sql(input_query).df()
    input_df = con.execute(input_query).df()
    st.dataframe(input_df)

    # on ne réagit que si un thème a été choisi
    if theme_selected:
        nb_lines_difference = solution_df.shape[0] - input_df.shape[0]
        if nb_lines_difference != 0:
            st.write(f"there are {nb_lines_difference} lines missing")

        # il reste à faire : tester si la réponse = la solution
        # 1ere idée : comparaison de tailles (colonnes puis lignes)
        if len(input_df.columns) != len(solution_df.columns):
            st.write("some columns are missing")

        # on choisit de mettre les colonnes de l'solution_df
        # dans le même ordre que celles de l'input_df
        # pour faciliter la comparaison après
        try:
            input_df = input_df[solution_df.columns]
        # bug si pas les mêmes colonnes
        except KeyError:
            st.write("some columns are missing")

    # Après un tour dans la doc pandas
    # nécessite que les noms de colonnes soient identiques
    # affiche le dataframe de comparaison des dataframes input et answer
    # probleme : si tailles des df différentes :
    # ValueError: Can only compare identically-labeled (both index and columns) DataFrame objects
    try:
        st.dataframe(input_df.compare(solution_df))
    # si ça bug sur une value error, on affiche juste son message
    except ValueError as e:
        st.write(f"{e}")


# -----------------------------------------------------------
# tabs présentant le contexte de l'exercice et la solution
# -----------------------------------------------------------
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    # on affiche les tables de l'exercice sélectionné
    # on utilise la méthode loc des df pour sortir la première ligne dans la colonne tables
    # rappel : tables contient la liste des tables associées à un exercice
    if theme_selected:
        # ici on a parfois des listes stockées sous forme de string -> ast.litteral_eval()
        exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
        for table in exercise_tables:
            st.write(f"table: {table}")
            # on va chercher la table en SQL avec son nom : easy
            df_table = con.execute(f'SELECT * FROM "{table}"').df()
            st.dataframe(df_table)

        # Reste à afficher la table de la solution attendue
        st.write("table expected:")
        st.dataframe(solution_df)
# with tab3:
#     st.write(ANSWER_QUERY)
