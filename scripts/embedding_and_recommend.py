import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

TEAM_TEXTS_PATH = "data/team_texts.json"

# 포지션별 키워드 사전
pos_keywords = {
    "중앙 미드필더": ["점유율", "빌드업", "짧은 패스", "중원 지배"],
    "수비수": ["조직적인 수비", "태클", "클리어링", "라인 컨트롤"],
    "공격수": ["빠른 침투", "골 결정력", "역습", "마무리", "드리블 돌파"]
}

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def load_team_texts():
    with open(TEAM_TEXTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data  # dict { 팀명: "감독 스타일: ..., 포메이션: ..., 팀 스타일: ..." }

def build_embeddings_dict(team_texts):
    embeddings_dict = {}
    for team_name, text in team_texts.items():
        team_emb = model.encode(text)
        embeddings_dict[team_name] = team_emb
    return embeddings_dict

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def recommend_teams(user_input, user_position, embeddings_dict, top_n=3):
    # (방법 A) 포지션 키워드 추가
    if user_position in pos_keywords:
        pos_terms = " ".join(pos_keywords[user_position])
        user_input += " " + pos_terms

    # 사용자 문장 임베딩
    user_emb = model.encode(user_input)

    scores = []
    for team_name, team_emb in embeddings_dict.items():
        sim = cosine_similarity(user_emb, team_emb)
        scores.append((team_name, sim))

    # 점수 높은 순 정렬
    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:top_n]

def main():
    # 1) 팀 텍스트 로드
    team_texts = load_team_texts()

    # 2) 팀별 임베딩
    embeddings_dict = build_embeddings_dict(team_texts)
    print(f"✅ 팀 임베딩 {len(embeddings_dict)}개 생성 완료.")

    # 3) 테스트 사용자 입력
    user_input = "나는 체력은 괜찮고, 짧은 패스를 좋아해"
    user_position = "중앙 미드필더"

    results = recommend_teams(user_input, user_position, embeddings_dict, top_n=3)

    # 4) 결과 표시
    print(f"\n🔎 사용자 입력: \"{user_input}\" (포지션: {user_position})")
    print("🎉 추천 팀 Top3:")
    for (team_name, score) in results:
        print(f" - {team_name}: {score:.3f}")

if __name__ == "__main__":
    main()
