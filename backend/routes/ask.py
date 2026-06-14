from fastapi import APIRouter
from pydantic import BaseModel

from backend.database.duckdb_manager import con
from backend.agents.sql_agent import get_schema
from backend.services.llm_service import generate_sql
from backend.agents.chart_agent import (suggest_chart,build_chart)


router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(
    req: QuestionRequest
):

    schema = get_schema()

    sql = generate_sql(
        schema,
        req.question
    )
    print("Generated SQL:")
    print(sql)
    result = con.execute(
        sql
    ).fetchdf()

    from backend.agents.insight_agent import generate_insight

    rows = result.to_dict(
        orient="records"
    )

    insight = generate_insight(
        req.question,
        rows
    )

    chart_type = suggest_chart(
        req.question,
        rows
    )

    chart = build_chart(
        rows,
        chart_type
    )
    
    chart_type = suggest_chart(
    req.question,
    rows
)

    insight = generate_insight(
            req.question,
            rows
        )

    return {
        "question": req.question,
        "sql": sql,
        "rows": rows,
        "insight": insight,
        "chart": chart
    }