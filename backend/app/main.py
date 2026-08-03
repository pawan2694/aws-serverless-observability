from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard import router as dashboard_router
from app.api.rag import router as rag_router

app = FastAPI(
    title="AWS Serverless Observability API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(rag_router)


@app.get("/")
def read_root():
    return {
        "message": "AWS Serverless Observability API",
        "status": "ok",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }