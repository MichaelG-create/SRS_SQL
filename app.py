# https://srssql.streamlit.app/
import streamlit as st
import pandas as pd
import duckdb

# st.write("Hello world")
data = {"a" : [1, 2, 3], "b" : [4, 5, 6]}
df = pd.DataFrame(data)

st.write("""
# SRS SQL 
Spaced Repetion System SQL practice
""")

tab1, tab2, tab3 = st.tabs (["Theme Selection", "Questions", "fish"])

with tab1:
    option = st.selectbox(
        "What would you like to review?",
        ["Joins", "GroupBy", "Window Functions"],
        index=None, # Default choice is None
        placeholder="Select what you want to review"
    )
    st.write("You selected:", option)

with tab2:
    sql_query = st.text_area(label = "type your code here")
    if sql_query != "":
        result = duckdb.sql(sql_query).df()
    else :
        result = pd.DataFrame({})
    st.write(f"Vous avez entré la query suivante :{sql_query}")

    # 2 options pour afficher un dataframe (kifkif)
    # st.dataframe(df)
    st.dataframe(result)

