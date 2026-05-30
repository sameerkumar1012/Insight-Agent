from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from pydantic import BaseModel

import pandas as pd

from cleaner import (
    clean_data,
    calculate_profit
)

from analyst import (
    analyze_question
)

app = FastAPI()

df = None


# HOME ROUTE
@app.get("/")
def home():

    return {
        "message": "CSV Analyst Agent Running"
    }


# UPLOAD CSV
@app.post("/upload")
async def upload_csv(
    file: UploadFile = File(...)
):

    global df

    # read csv
    df = pd.read_csv(file.file)

    # clean dataframe
    df = clean_data(df)

    # calculate profit
    df = calculate_profit(df)

    # remove NaN values
    df = df.fillna(0)

    return {
        "status": "success",
        "rows": len(df),
        "columns": list(df.columns),
        "preview": df.head().to_dict(
            orient="records"
        )
    }


# QUESTION MODEL
class Question(BaseModel):

    question: str


# ASK QUESTIONS
@app.post("/ask")
def ask_question(q: Question):

    global df

    # check if csv uploaded
    if df is None:

        return {
            "error": "Upload CSV first"
        }

    # analyze question
    answer = analyze_question(
        df,
        q.question
    )

    return {
        "question": q.question,
        "answer": answer
    }  