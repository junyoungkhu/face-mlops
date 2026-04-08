# 파이썬 3.11 슬림 이미지를 사용하여 빌드 용량 최적화
FROM python:3.11-slim

# 작업 디렉터리 설정
WORKDIR /app

# 파이썬 환경 변수 설정
# PYTHONDONTWRITEBYTECODE: .pyc 캐시 파일 생성을 방지
# PYTHONUNBUFFERED: 파이썬 출력을 버퍼링 없이 즉시 출력 (런타임 로그 확인용)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 전체 코드를 복사하기 전 requirements.txt만 우선 복사
# 이렇게 하면 소스코드가 변경되어도 패키지가 변경되지 않았다면 Docker 레이어 캐시를 재사용하여 속도가 매우 빨라집니다.
COPY requirements.txt .

# 종속성 설치 (파이프라인 안에서는 --no-cache-dir을 사용하여 불필요한 이미지 용량 팽창 방지)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 컨테이너 내 통신 포트
EXPOSE 8000

# uvicorn 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
