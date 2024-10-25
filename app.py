# https://srssql.streamlit.app/
import streamlit as st
import pandas as pd
import duckdb
import io

# PARTIE DATA
# ajout de vrai data pour les questions
csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages  = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie, 2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.sql(answer).df()


# ajout d'un header pour poser la question
st.header("enter your code:")
query = st.text_area(label="your SQL code here", key = "user_input")
# key = user_input sert à nommer la clé du widget (pour le retrouver après)

# test si la query n'est pas vide
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

# il reste à faire : tester si la réponse = la solution

# tabs présentant le contexte de l'exercice et la solution
tab2, tab3 = st.tabs (["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution)

with tab3:
    st.write(answer)



