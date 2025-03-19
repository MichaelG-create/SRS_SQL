# pylint: disable=missing-module-docstring

import duckdb

con = duckdb.connect(database="data/sql_exercises.duckdb", read_only=False)
# test = con.execute("SELECT * FROM beverages").df()
test = con.execute("SELECT * FROM sizes").df()
print(test)
