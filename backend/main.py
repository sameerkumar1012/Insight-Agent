from fastapi import FastAPI
from backend.routes.ask import router as ask_router

from backend.routes.upload import router as upload_router
from backend.routes.debug import router as debug_router
from backend.routes.schema import router as schema_router
from backend.routes.query import router as query_router


app = FastAPI()

app.include_router(upload_router)
app.include_router(query_router)
app.include_router(debug_router)
app.include_router(schema_router)
app.include_router(ask_router)

@app.get("/")
def home():
    return {
        "message": "Insight Agent 2.0 Running"
    }