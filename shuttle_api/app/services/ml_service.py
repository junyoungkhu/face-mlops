def predict_boarding_capacity(stop_name: str, time_of_day: str) -> dict:
    """
    MLOps 파이프라인에서 학습된 모델을 통해 정류장의 대기 인원 및 접근하는 버스의 잔여 용량을 예측합니다.
    현재는 더미(Dummy) 예측 로직을 반환합니다.
    """
    # TODO: joblib, MLflow, 혹은 Triton Inference Server 등으로 모델을 로드하여 실제 추론을 수행하도록 수정
    if "08" <= time_of_day[:2] < "10" and stop_name == "기숙사":
        return {
            "expected_waiting": 45,
            "bus_capacity_left": 10,
            "congestion_level": "만석(탑승 불가 다수 예상)"
        }
    
    return {
        "expected_waiting": 15,
        "bus_capacity_left": 40,
        "congestion_level": "여유"
    }
