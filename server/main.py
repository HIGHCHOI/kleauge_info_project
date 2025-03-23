# server/main.py
# uvicorn server.main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# 임베딩/추천 로직 가져오기
from .recommend_logic import init_model, recommend_teams

# FastAPI 앱 생성
app = FastAPI(
    title="K-League Recommendation API",
    version="1.0.0"
)

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중 전체 허용. 배포 시 ["http://localhost:5173"] 등으로 제한
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (POST, OPTIONS 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

# ✅ 사용자 요청 스키마 정의
class RecommendRequest(BaseModel):
    position: Optional[str] = None  # 예: "중앙 미드필더"
    style: str                      # 예: "점유율 축구, 전방 압박"

# ✅ 임베딩 저장 변수 (서버 시작 시 로드)
embeddings_dict = None

# ✅ 서버 시작 시 임베딩 불러오기
@app.on_event("startup")
def on_startup():
    global embeddings_dict
    embeddings_dict = init_model()  # team_summary의 벡터 임베딩 로드

# ✅ 추천 API
@app.post("/recommend")
def recommend(request: RecommendRequest, top_n: int = 3):
    """
    추천 요청 예시:
    POST /recommend?top_n=3
    {
      "position": "중앙 미드필더",
      "style": "나는 점유율과 빌드업 축구를 좋아해요"
    }
    """
    results = recommend_teams(
        user_input=request.style,
        user_position=request.position,
        embeddings_dict=embeddings_dict,
        top_n=top_n
    )
    return {"recommendations": results}
