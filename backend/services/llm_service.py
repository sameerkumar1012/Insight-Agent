from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

print("MODEL CREATED")
print(model)


def generate_sql(schema, question):

    prompt = f"""
You are a DuckDB SQL expert.

Table Schema:

{schema}

Rules:
1. Return ONLY SQL
2. No markdown
3. No explanation
4. No code fences
5. Use table name sales

Question:
{question}
"""

    print("generate_sql called")

    response = model.generate_content(
        prompt
    )

    print("response received")

    sql = response.text.strip()

    print("RAW SQL:")
    print(sql)

    sql = sql.replace(
        "```sql",
        ""
    )

    sql = sql.replace(
        "```",
        ""
    )

    return sql.strip()