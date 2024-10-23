import streamlit as st
import duckdb

tab1, tab2, tab3 = st.tabs (["cat", "dog", "fish"])

with tab1:
    st.write(input)
    input = st.text_area(label = "type your code here")


# query = (
# """"""
# input_user
# """"""
# )
# df = duckdb.sql(query).df()