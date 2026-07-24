from fastapi import FastAPI

from app.api.dashboard import router as dashboard_router

app = FastAPI(
    title="AWS Serverless Observability API"
)

app.include_router(dashboard_router)


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