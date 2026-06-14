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
You are an expert Business Intelligence SQL Analyst.

Table Schema:

{schema}

Table Name:
sales

Rules:
1. Return ONLY valid DuckDB SQL.
2. No markdown.
3. No explanations.
4. Use aggregation when questions ask for:
   - top products
   - most profitable products
   - highest revenue
   - best performing products
   - totals
   - averages
5. Always use GROUP BY when calculating metrics by product.
6. Use aliases like total_profit, total_sales, avg_price.
7. Prefer business-level summaries over row-level records.

Examples:

Question: Top profitable products

SQL:
SELECT
    product,
    SUM(profit) AS total_profit
FROM sales
GROUP BY product
ORDER BY total_profit DESC
LIMIT 5;

Question: Total profit by product

SQL:
SELECT
    product,
    SUM(profit) AS total_profit
FROM sales
GROUP BY product
ORDER BY total_profit DESC;

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