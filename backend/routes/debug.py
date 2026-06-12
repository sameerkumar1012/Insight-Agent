from fastapi import APIRouter
from backend.database.duckdb_manager import con

router = APIRouter()

@router.get("/tables")
def tables():

    return {
        "tables":
        con.execute("SHOW TABLES").fetchall()
    }


@router.get("/preview")
def preview():

    df = con.execute(
        "SELECT * FROM sales LIMIT 5"
    ).fetchdf()

    return df.to_dict(
        orient="records"
    )