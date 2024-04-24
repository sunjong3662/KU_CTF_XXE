### 문제 이름 : Fake Arasaka
### 환경 : Linux, Python
### 유형 : 웹 - XML eXternel Entity attack

# 유의사항 
- 현재 github에 올라와있는 파일에는 정답 파일(Flag file)을 빼놓을 예정입니다. 물론 정답이 뭐가 필요하겠냐만, 만약 정답이 나중에라도 필요하다 싶으면 아래의 이메일로 연락 주세요.
  - bulletproofbear@bulletproofyuri.kr
  - afhhddjjfdj@gmail.com
 
- 기본적으로 Linux의 환경이면 docker-compose가 깔려있어야 하며, docker desktop도 같이 깔려 있어야 합니다. docker 다운로드 방법은 docker 홈페이지를 참고해주시길 바랍니다.

- 지금 이 레포에는 주석 있는버전하고 없는 버전 2개의 브렌치가 있습니다. 처음에는 주석 없이 보시다가, 어려우면 힌트삼아서 주석 있는 버전을 보면서 공부하시면 좋을 듯 합니다...

- 근데, 이번이 처음 짜보는 코드고 그 만큼 부족하고 왜 이따구로 만들었지? 싶은 곳이 정말 많을겁니다.....

- 문의 정말 환영입니다.. 훈수는 더더욱 환영입니다...  개발 능력 올리려고 일단 만들었지만, 이렇게 더럽게 만들줄은 저도 몰랐습니다...

- 그냥, github를 본격적으로 사용하는것도 처음이고, 대부분이 다 처음입니다.. 
 
--- 

# 구성 방법.
1. ```git clone https://github.com/sunjong3662/KU_CTF_XXE```
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
