# kleauge_info_project
사용자의 정보(이름, 포지션, 스타일)를 입력하면 사용자의 스타일과 유사한 축구팀을 추천해주는 웹사이트.

# 추가하면 좋을 기능
기사에서 감독 인터뷰
선수들의 수준
자기 포지션의 현재 팀의 선수
연령별 ai 컨설턴트
축구선수가 아닌 축구와 관련된 진로 (실제 사례 추가)
개인 트레이너 연결(오픈 채팅방)

# 기본 설정
가상환경 : st
터미널 2개 사용
터미널1: 백엔드 (kleague_info_project폴더에서 “uvicorn server.main:app -reload”실행)
터미널2: 프론트엔드 (my-react-app폴더에서 “npm run dev” 실행)
참고로, scripts폴더에 있는 파이썬 파일들을 실행할 때, 터미널에서 다음과 같이 실행
python scripts/~.py
참고로, 다운받은 패키지를 보관하고 싶다면, 터미널에서 다음과 같이 실행
전체 저장: pip freeze > requirements.txt
일부 저장: pip freeze | grep -E “원하는 패키지" >> requirements.txt

# 구현 과정
1. k1 / k2 / k3 league 소속 팀명 수동 수집 
kleague_info_project/scripts/collect_team_list.py

리그 별 팀 목록 생성
kleague_info_project/data/teams/k1_teams.json
kleague_info_project/data/teams/k2_teams.json
kleague_info_project/data/teams/k1_teams.json


2. 팀&감독 나무 위키 링크 수동 수집
kleague_info_project/data/teams/team_links_manual.json


3. Selenium 사용하여 팀&감독 나무위키 본문을 .txt로 저장
kleague_info_project/scripts/extract_team_info.py

팀별로 팀&감독 나무위키 본문 내용을 하나로 합친 .txt 저장
kleague_info_project/data/teams_summary/FC 서울.txt
kleague_info_project/data/teams_summary/수원 삼성 블루윙즈.txt
….


4. OpenRouter API (deepseek-r1-zero:free)를 통해 팀&감독 본문을 요약하고, 구조화된 JSON형태로 저장
성공한 팀은 data/team_summaries에 실패한 팀은 data/team_summaries_errors에 저장
kleague_info_project/scripts/summarize_team_info.py

kleague_info_project/data/teams_summaries/FC 서울.json
kleague_info_project/data/teams_summaries/수원 삼성 블루윙즈.json
….

kleague_info_project/data/teams_summaries_errors


5. teams_summaries_errors에 있는 실패한 .txt파일의 구조를 .json구조에 맞게 간단한 수정을 한 뒤, .json파일로 바꿔서 teams_summaries에 넣는다. 이때, 아무 파일에도 들어가지 않고 응답에 실패한 .txt파일들을 대상으로 한번 더 summarize_team_info.py을 실행한다.


6. data/teams_summaries에 있는 팀별 .json파일들을 
{
    “팀 이름”: “감독 스타일:    , 포메이션:    , 팀 스타일:    “,
    “팀 이름”: “감독 스타일:    , 포메이션:    , 팀 스타일:    “,
    “팀 이름”: “감독 스타일:    , 포메이션:    , 팀 스타일:    “,
    …..
}
위와 같은 .json형식으로 만들어서 data폴더에 저장한다.

kleague_info_project/scripts/create_team_text.py

kleague_info_project/data/team_texts.json


7. Sentence Transformers라이브러리와 all-MiniLM-L6-v2모델을 이용하여 data/team_texts.json에 대한텍스트 임베딩을 수행하고, 사용자의 입력을 받아 임베딩으로 변환한 뒤, 두 임베딩 간의 유사도를 계산하여, 사용자의 스타일을 바탕으로 적합한 축구팀을 추천하는 알고리즘을 구현.
kleague_info_project/scripts/embedding_and_recommend.py


8. Frontend + Backend PipeLine
 Frontend: kleague_info_project/my-react-app/src/App.jsx
Backend: kleague_info_project/server/main.py
	    kleague_info_project/server/recommend_logic.py

[사용자 입력]
   │
   ▼
[React 프론트엔드]
   │        (POST /recommend)
   ▼
[FastAPI 백엔드]
   │
   ├── “팀 요약 벡터”와 “유저 벡터” 간 유사도 계산
   ▼
[추천 결과]
   │
   ▼
[React에 JSON 응답]
   │
   ▼
[추천 카드 UI로 출력]


# 파일구조
https://github.com/user-attachments/assets/f07c4f73-7b2a-4a67-9e6a-72e92d62087a
