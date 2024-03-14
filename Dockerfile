FROM python:3.9-slim
MAINTAINER "bulletproofbear@bulletproofyuri.kr"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#사실 flag파일로 둘까 생각했지만, 그냥 echo로 넣는다. ++ 권한
RUN echo "KUCTF{deleted flag.}" > /etc/myrealpc
RUN chmod 755 /etc/myrealpc


COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
