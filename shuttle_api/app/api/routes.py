from fastapi import APIRouter, Depends
from typing import List
from app.models.schemas import BusTimetable, StopStatus, BoardPredictRequest
from app.services.ml_service import predict_boarding_capacity

router = APIRouter()

@router.get("/timetable/{route_id}", response_model=List[BusTimetable])
def get_timetable(route_id: str):
    """기본 노선 시간표 조회"""
    # 실제 DB 연동 부분
    return [
        {"bus_id": "BUS-01", "route_name": route_id, "departure_time": "08:00", "arrival_time": "08:15"},
        {"bus_id": "BUS-02", "route_name": route_id, "departure_time": "08:15", "arrival_time": "08:30"}
    ]

@router.post("/stops/status", response_model=StopStatus)
def get_stop_status(request: BoardPredictRequest):
    """
    정류장별 대기 인원 및 버스 여유 공간을 예측하여 탑승 제한을 반영한 상태를 반환합니다.
    MLOps 파이프라인의 Inference 결과를 활용합니다.
    """
    prediction = predict_boarding_capacity(request.stop_name, request.time_of_day)
    
    can_board = prediction["bus_capacity_left"] > prediction["expected_waiting"]
    
    return StopStatus(
        stop_name=request.stop_name,
        expected_waiting=prediction["expected_waiting"],
        bus_capacity_left=prediction["bus_capacity_left"],
        can_board=can_board,
        congestion_level=prediction["congestion_level"]
    )
