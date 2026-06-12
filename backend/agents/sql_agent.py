from backend.database.duckdb_manager import con


def get_schema():

    schema = con.execute(
        "DESCRIBE sales"
    ).fetchall()

    schema_text = "\n".join(
        [
            f"{col[0]} {col[1]}"
            for col in schema
        ]
    )

    return schema_text


def get_prompt(schema, question):

    return f"""
You are a DuckDB SQL expert.

Table Schema:

{schema}

Rules:
1. Generate only valid DuckDB SQL
2. Use table name sales
3. Return only SQL
4. No explanation

Question:
{question}
"""