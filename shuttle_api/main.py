from fastapi import FastAPI
from app.api.routes import router as shuttle_router

app = FastAPI(
    title="Campus Shuttle Bus API",
    description="교내 셔틀버스 기본 노선 및 ML 기반 탑승 인원 예측 API",
    version="1.0.0"
)

app.include_router(shuttle_router, prefix="/api/v1/shuttle", tags=["Shuttle"])

@app.get("/")
def read_root():
    return {"message": "API is running. Visit /docs for Swagger UI."}

# Trigger deployment
