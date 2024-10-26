# pylint: disable=missing-module-docstring

import io

import pandas as pd
import duckdb


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# -------------------------------------------------------------
# EXERCISES LIST
# -------------------------------------------------------------
data = {
    "theme": ["cross_joins"],
    "exercise_name": ["beverages_and_food"],
    "tables": [["beverages", "food_items"]],
    "last_reviewed": ["1970-01-01"]
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# -------------------------------------------------------------
# CROSS JOIN EXERCISES
# -------------------------------------------------------------
# ajout de vrai data pour les questions
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))
# Table creation in the real db
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie, 2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
# Table creation in the real db
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")


ANSWER_QUERY = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
answer_df = duckdb.sql(ANSWER_QUERY).df()
