"""
OpenRouter API (deepseek-r1-zero:free)를 통해 팀+감독 본문을 요약하고,
구조화된 JSON으로 저장합니다. 실패한 팀은 별도 폴더에 기록됩니다.
"""

import os
import json
import time
import re
import openai
from dotenv import load_dotenv

# 1) .env.local에서 API 키 읽기
load_dotenv(".env.local")
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# 2) 폴더 설정
INPUT_DIR = "data/teams_summary"
OUTPUT_DIR = "data/team_summaries"
ERROR_DIR = "data/team_summaries_errors"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ERROR_DIR, exist_ok=True)

# 3) 사용할 모델
MODEL = "deepseek/deepseek-r1-zero:free"

# 4) 요약할 항목들 안내 프롬프트
def make_prompt(text):
    return f"""
다음은 한국 축구팀의 팀 및 감독 소개입니다. 이 정보를 바탕으로 다음 항목들을 JSON 형식으로 추출해 주세요:

1. 팀이름
2. 감독
3. 감독 스타일 (예: 전방 압박, 수비적, 빌드업 중심 등)
4. 포메이션 (예: 4-4-2, 3-5-2 등)
5. 팀 스타일 (예: 점유율 기반, 역습, 롱패스 중심, 측면 공격 등 전략 포함)

형식 예시는 다음과 같습니다:

{{
  "team_name": "FC 서울",
  "manager": "김기동",
  "manager_style": "공격적이고 전방 압박을 지향함",
  "formation": "4-3-3",
  "team_style": "측면을 활용한 빠른 역습 중심 전개, 점유율보다 속도 중시"
}}

본문:
{text.strip()}
"""

# 5) 응답에서 JSON 부분만 안전하게 추출하기
def extract_json_string(raw_text: str) -> str:
    """
    모델 응답에서 JSON 구조를 최대한 안정적으로 추출하는 함수.
    - \boxed{...}
    - ```json ...
    - 이중/삼중 중괄호
    - 배열([]) 형태
    - 등등을 정규식을 통해 정리
    """

    # 1) \boxed{ 제거 → 여유 있게 여러 개 중첩 가능성 대비
    # \boxed{{{ => {
    text = re.sub(r"\\?boxed\s*\{+", "{", raw_text)

    # 2) 백틱 제거 (```json, ``` 등)
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    text = text.strip("`\n ").strip()

    # 3) 이중/삼중 중괄호 제거
    # 예) {{{ ... }}} → { ... }
    while text.startswith("{") and text.endswith("}}"):
        text = text[:-1]
    while text.startswith("{{"):
        text = text[1:]

    # 4) 혹시 배열([])로 감싸져 있는 경우 → 첫 요소만 꺼내기
    candidate = text.strip()
    if candidate.startswith("[") and candidate.endswith("]"):
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, list) and len(parsed) > 0:
                # 리스트의 첫 번째만 반환
                return json.dumps(parsed[0], ensure_ascii=False)
        except:
            pass

    return text

# 6) OpenRouter 요약 호출
def summarize(text):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": make_prompt(text)}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] 요약 실패: {e}")
        return None

# 7) 메인 로직
def main():
    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".txt"):
            continue

        team_name = filename.replace(".txt", "")
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, f"{team_name}.json")

        print(f"🧠 {team_name} 요약 중...")

        # 원본 텍스트 로딩
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        # AI 요약
        summary_text = summarize(text)
        if not summary_text:
            print(f"⚠️ {team_name} 요약 실패: 응답이 없음")
            continue

        # 파싱 시도
        try:
            # JSON만 추출
            cleaned_text = extract_json_string(summary_text)
            # 실제 파싱
            summary_json = json.loads(cleaned_text)

            # 결과 저장
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(summary_json, f, ensure_ascii=False, indent=2)

            print(f"✅ {team_name} 요약 저장 완료")

        except Exception as e:
            print(f"[ERROR] JSON 파싱 실패 ({team_name}): {e}")
            print("⛔ 응답 내용:")
            print(summary_text)

            # 실패한 응답 별도 폴더에 저장
            error_txt = os.path.join(ERROR_DIR, f"{team_name}.txt")
            with open(error_txt, "w", encoding="utf-8") as ef:
                ef.write(summary_text)

            # 실패 로그
            with open(os.path.join(ERROR_DIR, "error_log.txt"), "a", encoding="utf-8") as log:
                log.write(f"{team_name}\n")

        time.sleep(1.5)  # 호출 간격 제한

if __name__ == "__main__":
    main()
