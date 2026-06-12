from fastapi import APIRouter
from backend.database.duckdb_manager import con

router = APIRouter()

@router.get("/schema")
def schema():

    result = con.execute(
        "DESCRIBE sales"
    ).fetchall()

    return {
        "table": "sales",
        "schema": result
    }