from fastapi import FastAPI
# Trigger redeploy for Runner fix
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api.routes import router as shuttle_router

app = FastAPI(
    title="Campus Shuttle Bus API",
    description="교내 셔틀버스 기본 노선 및 ML 기반 탑승 인원 예측 API",
    version="1.0.0"
)

# Static file serving config
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(shuttle_router, prefix="/api/v1/shuttle", tags=["Shuttle"])

@app.get("/")
def read_root():
    # 루트 접속 시 웹 프론트엔드로 즉시 리다이렉트
    return RedirectResponse(url="/static/index.html")
