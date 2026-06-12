import duckdb

con = duckdb.connect(
    database="analytics.db",
    read_only=False
)