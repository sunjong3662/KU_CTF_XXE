# Python 베이스 이미지를 사용합니다.
FROM python:3.10-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# Flask 앱의 의존성 파일을 컨테이너에 복사합니다.
COPY requirements.txt .

# 의존성을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 소스 코드를 컨테이너에 복사합니다.
COPY . .

RUN echo "KUCTF{XXE_1nj3ct1On_1S_3asY_F0r_us}" > /app/FLAG

# 5000번 포트를 외부로 노출합니다.
EXPOSE 5000

# Flask 앱을 실행합니다.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
