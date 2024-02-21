import os

bind = "0.0.0.0:5000"  # 서버가 바인딩할 호스트와 포트
workers = 4
accesslog = "-"  # 접근 로그를 표준 출력으로 설정
errorlog = "-"  # 에러 로그를 표준 출력으로 설정
