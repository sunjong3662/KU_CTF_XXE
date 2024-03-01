FROM python:3.9-slim
MAINTAINER "bulletproofbear@bulletproofyuri.kr"


# 작업 디렉토리 설정.
WORKDIR /app


#  의존성 + 소스코드들 싸그리 싺싺 복사 / 여기서 . 은 WORKDIR을 의미함.
COPY ./requirements.txt .
COPY ./file .
COPY ./flag/flag /etc/myrealpc

#/app으로 복사된 의존성안에 있는 텍스트 추출해다가 모두 설치
RUN pip install --no-cache-dir -r ./requirements.txt

# 필요한 실행 권한 설정
RUN chmod 755 /etc/myrealpc
RUN chmod +x ./init-mariadb.sh

# only 5000번만이 외부에 노출되는거임 ㅇㅇ
EXPOSE 5000

# gunicorn이용해서 5000번에 바인딩해서 외부에서 접속할 수 있게 하는거임...
# 기존의 app.py자체 실행을 하는거 대신에 그냥 바로 5000번 열어다가 url로 접속하게 되면 나오게 하는거임.. app:app이 저거임.
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
