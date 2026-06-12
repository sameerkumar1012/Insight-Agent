from backend.services.llm_service import model


def generate_insight(
    question,
    data
):

    prompt = f"""
You are a Senior Business Analyst.

Question:
{question}

Query Results:
{data}

Rules:
1. Use ONLY the information present in the query results.
2. Do NOT assume anything about the company.
3. Do NOT recommend expansion, diversification, marketing, or strategy unless clearly supported by the data.
4. Keep the response concise and professional.
5. If the result contains only a few rows, summarize them directly.
6. If no data is available, clearly state that.

Provide output in this format:

Summary:
<short summary>

Key Finding:
<main finding>

Recommendation:
<recommendation based only on the data>
"""

    response = model.generate_content(
        prompt
    )

    return response.text.strip()