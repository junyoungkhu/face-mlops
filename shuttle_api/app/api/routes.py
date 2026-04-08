from fastapi import APIRouter, Depends
from typing import List
from app.models.schemas import BusTimetable, StopStatus, BoardPredictRequest, CongestionFeedback, FeedbackResponse
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

@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(feedback: CongestionFeedback):
    """
    학생들이 체감하는 실시간 정류장/버스 혼잡도를 피드백 받습니다.
    접수된 피드백은 모델 재학습(Retraining) 또는 실시간 혼잡도 보정에 활용됩니다.
    """
    # 실제 환경에서는 DB에 저장하거나 Kafka 등의 메시지 큐로 전송하여 MLOps 재학습에 활용합니다.
    print(f"[Feedback Received] {feedback.stop_name} ({feedback.route_name}): {feedback.congestion_level}")
    if feedback.comments:
        print(f"Comments: {feedback.comments}")
        
    return FeedbackResponse(
        status="success",
        message="소중한 피드백이 접수되었습니다. 더 나은 셔틀버스를 위해 반영하겠습니다!"
    )
