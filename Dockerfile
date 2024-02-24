FROM ubuntu:20.04

# 환경 설정 및 Python 설치를 위한 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정.
WORKDIR /app

# Flask 앱의 의존성 파일 적은거 안에 복사함.
COPY requirements.txt .

# 복사한 저거 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt


RUN echo "KUCTF{XXE_1nj3ct1On_1S_3asY_F0r_us}" > /etc/myrealpc


# 소스코드들 싸그리 싺싺 복사
COPY . .

# only 5000번이 나올 수 있음.
EXPOSE 5000

# gunicorn이용해서 5000번에 바인딩해서 외부에서 접속할 수 있게 하는거임...
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
