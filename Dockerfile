FROM ubuntu:20.04

# 환경 설정 및 Python 설치를 위한 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# Flask 앱의 의존성 파일을 컨테이너에 복사합니다.
COPY requirements.txt .

# 의존성을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 소스 코드를 컨테이너에 복사합니다.
COPY . .

RUN echo '<flag>KUCTF{XXE_1nj3ct1On_1S_3asY_f0r_uS}</flag>' > /etc/myrealpc.xml

# 5000번 포트를 외부로 노출합니다.
EXPOSE 5000

# Flask 앱을 실행합니다.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
