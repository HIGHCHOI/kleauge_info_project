# server/recommend_logic.py

import os
import json
from sentence_transformers import SentenceTransformer, util

# 팀 요약 데이터 위치
SUMMARY_PATH = "data/team_summaries"

# SentenceTransformer 초기화
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def init_model():
    """
    팀 요약 텍스트 불러와서 임베딩 생성
    """
    embeddings_dict = {}

    for filename in os.listdir(SUMMARY_PATH):
        if filename.endswith(".json"):
            path = os.path.join(SUMMARY_PATH, filename)
            with open(path, "r", encoding="utf-8") as f:
                summary = json.load(f)

            team_name = summary["team_name"]
            # 하나의 문자열로 임베딩 생성
            full_text = f"{summary['manager_style']}. {summary['team_style']}"
            embedding = model.encode(full_text)
            embeddings_dict[team_name] = {
                "embedding": embedding,
                "summary": summary
            }

    return embeddings_dict


def recommend_teams(user_input, user_position, embeddings_dict, top_n=3):
    """
    사용자 입력 + 포지션 → 추천 결과
    """
    # 사용자 입력 + 포지션을 하나의 문장으로 결합
    query_text = f"{user_input}"
    if user_position:
        query_text = f"{user_position} 스타일: {user_input}"

    query_emb = model.encode(query_text)

    # 유사도 계산
    scored = []
    for team_name, data in embeddings_dict.items():
        score = util.cos_sim(query_emb, data["embedding"]).item()
        scored.append((team_name, score, data["summary"]))

    # 상위 N개 추출
    top_matches = sorted(scored, key=lambda x: x[1], reverse=True)[:top_n]

    # 출력 형식 변경
    return [
        {
            "team_name": name,
            "manager": summary.get("manager", "정보 없음"),
            "team_style": summary.get("team_style", "정보 없음"),
            "score": round(score, 3)
        }
        for name, score, summary in top_matches
    ]
