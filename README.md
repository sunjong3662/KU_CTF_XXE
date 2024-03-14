### 문제 이름 : Fake Arasaka
### 환경 : Linux, Python
### 유형 : 웹 - XML eXternel Entity attack

# 유의사항 
- 현재 github에 올라와있는 파일에는 정답 파일(Flag file)을 빼놓을 예정입니다. 물론 정답이 뭐가 필요하겠냐만, 만약 정답이 나중에라도 필요하다 싶으면 아래의 이메일로 연락 주세요.
  - bulletproofbear@bulletproofyuri.kr
  - afhhddjjfdj@gmail.com
 
- 기본적으로 Linux의 환경이면 docker-compose가 깔려있어야 하며, docker desktop도 같이 깔려 있어야 합니다. docker 다운로드 방법은 docker 홈페이지를 참고해주시길 바랍니다.
 
--- 

# 구성 방법.
1. git clone
   - 먼저 지금 git을 clone해서 문제 파일을 다운 받아줍니다.
   - 그 다음 다운 받아준 폴더 안으로 들어가줍니다.

   ``` cd KU_CTF_XXE ```

2. docker-compose
   - clone 한 파일로 들어왔으면, docker desktop을 켜줍니다.
   - 킨 것을 확인하셨으면, 폴더에서 docker-compose를 이용해서 문제를 구축하면 끝입니다.

   ``` docker-compose up --build ```

3. 종료.
   - 문제를 다 푸시거나, 마무리하고 싶으시다면 docker-compose down을 해주셔야 합니다.

   ``` docker-compose down ```


Write Up은 나중에 정리해서 올릴 예정입니다...
