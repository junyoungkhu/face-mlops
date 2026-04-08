from pydantic import BaseModel, Field

class BusTimetable(BaseModel):
    bus_id: str
    route_name: str
    departure_time: str
    arrival_time: str

class BoardPredictRequest(BaseModel):
    stop_name: str
    time_of_day: str = Field(description="조회하려는 시간 (예: 08:30)")
    day_of_week: str = Field(default="MON", description="요일 (예: MON, TUE)")

class StopStatus(BaseModel):
    stop_name: str
    expected_waiting: int = Field(description="예측된 대기 인원 수")
    bus_capacity_left: int = Field(description="현재 접근 중인 버스의 잔여 좌석 수")
    can_board: bool = Field(description="전원 탑승 가능 여부")
    congestion_level: str = Field(description="혼잡도 수준 (예: 여유, 보통, 혼잡, 만석)")
