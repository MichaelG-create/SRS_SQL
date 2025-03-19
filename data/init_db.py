# pylint: disable=missing-module-docstring

import io

import duckdb
import pandas as pd

con = duckdb.connect(database="data/sql_exercises.duckdb", read_only=False)

# -------------------------------------------------------------
# EXERCISES LIST
# -------------------------------------------------------------
EXERCISES = {
    "theme": [
        "cross_joins",
        "cross_joins",
    ],
    "name": [
        "beverages_and_food",
        "trademarks_and_sizes",
    ],
    "tables_names": [
        ["beverages", "food_items"],
        ["trademarks", "sizes"],
    ],
    "last_reviewed": [
        "1970-01-02",
        "1970-01-01",
    ],
}
exercises_df = pd.DataFrame(EXERCISES)
con.execute("DROP TABLE IF EXISTS exercises")
con.execute("CREATE TABLE IF NOT EXISTS exercises AS SELECT * FROM exercises_df")

# -------------------------------------------------------------
# CROSS JOIN EXERCISE
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
con.execute("DROP TABLE IF EXISTS beverages")
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie, 2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
# Table creation in the real db
con.execute("DROP TABLE IF EXISTS food_items")
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")
# -------------------------------------------------------------
# ANOTHER CROSS JOIN EXERCISE (
# -------------------------------------------------------------
# ajout de vrai data pour les questions
SIZES = """
size
XS
M
L
XL
"""
SIZES = pd.read_csv(io.StringIO(SIZES))
con.execute("DROP TABLE IF EXISTS sizes")
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM SIZES")

TRADEMARKS = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
TRADEMARKS = pd.read_csv(io.StringIO(TRADEMARKS))
con.execute("DROP TABLE IF EXISTS trademarks")
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM TRADEMARKS")

con.close()
