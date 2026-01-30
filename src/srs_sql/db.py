# pylint: disable=missing-module-docstring
import io
import os
from pathlib import Path

import duckdb
import pandas as pd
import yaml


DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "sql_exercises.duckdb"
BASE_DIR = Path(__file__).resolve().parent
EXERCISES_YAML = BASE_DIR / "config" / "exercises.yml"



def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Ensure data dir exists and return an open DuckDB connection.
    """
    DATA_DIR.mkdir(exist_ok=True)
    con = duckdb.connect(database=str(DB_PATH), read_only=False)
    return con


def init_base_tables(con: duckdb.DuckDBPyConnection) -> None:
    """
    Create / refresh base tables used in exercises (small CSV-like data).
    Idempotent: safe to run multiple times.
    """
    # ------------------------------------------------------------------
    # CROSS JOIN EXERCISES
    # ------------------------------------------------------------------
    CSV_BEV = """beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
    beverages = pd.read_csv(io.StringIO(CSV_BEV))
    con.execute("DROP TABLE IF EXISTS beverages")
    con.execute("CREATE TABLE beverages AS SELECT * FROM beverages")

    CSV_FOOD = """food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
"""
    food_items = pd.read_csv(io.StringIO(CSV_FOOD))
    con.execute("DROP TABLE IF EXISTS food_items")
    con.execute("CREATE TABLE food_items AS SELECT * FROM food_items")

    SIZES = """size
XS
M
L
XL
"""
    sizes = pd.read_csv(io.StringIO(SIZES))
    con.execute("DROP TABLE IF EXISTS sizes")
    con.execute("CREATE TABLE sizes AS SELECT * FROM sizes")

    TRADEMARKS = """trademark
Nike
Asphalte
Abercrombie
Lewis
"""
    trademarks = pd.read_csv(io.StringIO(TRADEMARKS))
    con.execute("DROP TABLE IF EXISTS trademarks")
    con.execute("CREATE TABLE trademarks AS SELECT * FROM trademarks")

    # ------------------------------------------------------------------
    # EMPLOYEES (basic select + filtering)
    # ------------------------------------------------------------------
    EMPLOYEES = """employee_id,first_name,last_name,department,salary,hire_date
1,Alice,Martin,Engineering,65000,2020-01-15
2,Bob,Dupont,Marketing,52000,2019-03-10
3,Claire,Durand,Engineering,72000,2021-07-01
4,David,Petit,HR,48000,2018-11-20
5,Emma,Leroy,Sales,55000,2022-05-05
"""
    employees = pd.read_csv(io.StringIO(EMPLOYEES))
    con.execute("DROP TABLE IF EXISTS employees")
    con.execute("CREATE TABLE employees AS SELECT * FROM employees")

    # ------------------------------------------------------------------
    # ORDERS / CUSTOMERS (aggregations + joins)
    # ------------------------------------------------------------------
    ORDERS = """order_id,customer_id,order_date,amount,status
1001,1,2024-01-10,120.5,shipped
1002,2,2024-01-11,75.0,shipped
1003,1,2024-01-12,210.0,cancelled
1004,3,2024-01-13,50.0,processing
1005,2,2024-01-14,320.0,shipped
1006,3,2024-01-15,40.0,processing
"""
    orders = pd.read_csv(io.StringIO(ORDERS))
    con.execute("DROP TABLE IF EXISTS orders")
    con.execute("CREATE TABLE orders AS SELECT * FROM orders")

    CUSTOMERS = """customer_id,customer_name,country
1,ACME Corp,FR
2,Globex,DE
3,Innotech,UK
"""
    customers = pd.read_csv(io.StringIO(CUSTOMERS))
    con.execute("DROP TABLE IF EXISTS customers")
    con.execute("CREATE TABLE customers AS SELECT * FROM customers")

    # ------------------------------------------------------------------
    # SALES (window + procedural-style)
    # ------------------------------------------------------------------
    SALES = """sale_id,customer_id,sale_date,amount
1,1,2024-01-01,100
2,1,2024-01-05,150
3,1,2024-01-10,200
4,2,2024-01-03,80
5,2,2024-01-08,120
6,3,2024-01-02,50
7,3,2024-01-09,70
"""
    sales = pd.read_csv(io.StringIO(SALES))
    con.execute("DROP TABLE IF EXISTS sales")
    con.execute("CREATE TABLE sales AS SELECT * FROM sales")

    # ------------------------------------------------------------------
    # PRODUCTS (DDL)
    # ------------------------------------------------------------------
    PRODUCTS = """product_id,product_name,unit_price,active
10,Keyboard,45.0,true
11,Mouse,25.0,true
12,Monitor,220.0,true
13,Cable,5.0,false
"""
    products = pd.read_csv(io.StringIO(PRODUCTS))
    con.execute("DROP TABLE IF EXISTS products")
    con.execute("CREATE TABLE products AS SELECT * FROM products")


def init_exercises(con: duckdb.DuckDBPyConnection) -> None:
    """
    Load exercise metadata from YAML and create the exercises table.
    """
    if not EXERCISES_YAML.exists():
        raise FileNotFoundError(f"Missing config file: {EXERCISES_YAML}")

    with EXERCISES_YAML.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    rows = []
    for ex in cfg["exercises"]:
        rows.append(
            {
                "theme": ex["theme"],
                "name": ex["name"],
                "tables_names": ex["tables"],
                "difficulty": ex["difficulty"],
                "last_reviewed": "1970-01-01",
                "instruction": ex["instruction"],
            }
        )

    exercises_df = pd.DataFrame(rows)
    con.execute("DROP TABLE IF EXISTS exercises")
    con.execute("CREATE TABLE exercises AS SELECT * FROM exercises_df")
