import os

import google.generativeai as genai

from dotenv import load_dotenv


# =====================================
# LOAD ENV VARIABLES
# =====================================

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not GEMINI_API_KEY:

    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


# =====================================
# CONFIGURE GEMINI
# =====================================

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# =====================================
# MAIN ANALYSIS FUNCTION
# =====================================

def analyze_question(df, question):

    query_prompt = f"""
You are an expert Pandas Data Analyst.

DataFrame columns:

{list(df.columns)}

User Question:
{question}

Your task:
Generate ONE executable pandas expression.

Rules:
1. Use dataframe name df
2. Return ONLY python code
3. No markdown
4. No explanation
5. No comments
6. No imports
7. No print statements
8. Expression must be executable with eval()

Examples:

Question:
What is total profit?

Output:
df["profit"].sum()

Question:
Which product has highest profit?

Output:
df.groupby("product")["profit"].sum().idxmax()

Question:
Show top 5 products by profit

Output:
df.groupby("product")["profit"].sum().sort_values(ascending=False).head(5)
"""

    try:

        # =====================================
        # STEP 1
        # GENERATE PANDAS CODE
        # =====================================

        response = model.generate_content(
            query_prompt
        )

        code = response.text.strip()

        code = (
            code
            .replace(
                "```python",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )

        print(
            "\n===================="
        )

        print(
            "GENERATED CODE"
        )

        print(
            "===================="
        )

        print(code)

        # =====================================
        # STEP 2
        # EXECUTE CODE
        # =====================================

        result = eval(
            code,
            {"df": df}
        )

        # =====================================
        # FORMAT RESULT
        # =====================================

        if hasattr(
            result,
            "head"
        ):

            result_text = (
                result.head(10)
                .to_string()
            )

        else:

            result_text = str(
                result
            )

        print(
            "\n===================="
        )

        print(
            "RAW RESULT"
        )

        print(
            "===================="
        )

        print(
            result_text
        )

        # =====================================
        # STEP 3
        # BUSINESS EXPLANATION
        # =====================================

        explanation_prompt = f"""
You are a senior business analyst.

User Question:
{question}

Analysis Result:
{result_text}

Explain the answer in clear
business language.

Requirements:

- Keep answer concise
- Explain insights
- Mention trends if visible
- Avoid technical jargon
- If result is a table,
  summarize key findings

Return only the explanation.
"""

        explanation = (
            model.generate_content(
                explanation_prompt
            ).text.strip()
        )

        print(
            "\n===================="
        )

        print(
            "EXPLANATION"
        )

        print(
            "===================="
        )

        print(
            explanation
        )

        # =====================================
        # FINAL RESPONSE
        # =====================================

        return explanation

    except Exception as e:

        print(
            "\n===================="
        )

        print(
            "ANALYSIS ERROR"
        )

        print(
            "===================="
        )

        print(e)

        return (
            f"Error: {e}"
        )