import os
import json

INPUT_DIR = "data/team_summaries"
OUTPUT_FILE = "data/team_texts.json"

def create_team_texts():
    result = {}
    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".json"):
            continue
        
        filepath = os.path.join(INPUT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        team_name = data.get("team_name", filename.replace(".json", ""))
        manager = data.get("manager", "")
        manager_style = data.get("manager_style", "")
        formation = data.get("formation", "")
        team_style = data.get("team_style", "")

        # 하나의 문장으로 합치기
        # 필요하다면 필드를 더 추가할 수 있음 (ex. 구단 가치, 우승 경력 등)
        combined_text = (
            f"감독 스타일: {manager_style}, "
            f"포메이션: {formation}, "
            f"팀 스타일: {team_style}"
        )

        # 팀 이름을 key, 변환된 문장을 value로 저장
        result[team_name] = combined_text

    # 최종 결과를 JSON으로 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 팀별 텍스트 생성 완료 → {OUTPUT_FILE}")

if __name__ == "__main__":
    create_team_texts()
