from fastapi import APIRouter, UploadFile, File
import pandas as pd

from cleaner import (
    clean_data,
    calculate_profit
)

from backend.database.duckdb_manager import con
router = APIRouter()

@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...)
):

    df = pd.read_csv(file.file)

    df = clean_data(df)

    df = calculate_profit(df)

    df = df.fillna(0)

    con.execute(
        "CREATE OR REPLACE TABLE sales AS SELECT * FROM df"
    )
    print("Tables:", con.execute("SHOW TABLES").fetchall())
    
    return {
        "status": "success",
        "rows": len(df),
        "columns": list(df.columns)
    }