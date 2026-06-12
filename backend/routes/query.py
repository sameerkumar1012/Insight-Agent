from fastapi import APIRouter
from pydantic import BaseModel

from backend.database.duckdb_manager import con

router = APIRouter()


class SQLRequest(BaseModel):
    sql: str


@router.post("/query")
def run_query(req: SQLRequest):

    try:

        result = con.execute(
            req.sql
        ).fetchdf()

        return {
            "rows":
            result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        return {
            "error": str(e)
        }