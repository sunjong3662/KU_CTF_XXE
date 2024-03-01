FROM python:3.9-slim
MAINTAINER "bulletproofbear@bulletproofyuri.kr"


# 작업 디렉토리 설정.
WORKDIR /app

# Flask 앱의 의존성 파일 적은거 안에 복사함. (. 은 저기 WORKDIR정한거 와일드카드 형식으로 간략화 한거.)
COPY requirements.txt .

#/app으로 복사된 의존성안에 있는 텍스트 추출해다가 모두 설치
RUN pip install --no-cache-dir -r requirements.txt

#사실 flag파일로 둘까 생각했지만, 그냥 echo로 넣는다. ++ 권한
RUN echo "KUCTF{XXE_1nj3ct1On_1S_3@sY_F0r_uS}" > /etc/myrealpc
RUN chmod 755 /etc/myrealpc


# 소스코드들 싸그리 싺싺 복사
COPY . .

# only 5000번이 나올 수 있음.
EXPOSE 5000

# gunicorn이용해서 5000번에 바인딩해서 외부에서 접속할 수 있게 하는거임...
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
