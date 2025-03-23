"""
Selenium을 사용하여 팀과 감독의 나무위키 페이지 본문을 추출하고 하나의 텍스트 파일로 저장합니다.
"""

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 파일 경로 설정
INPUT_PATH = "data/teams/team_links_manual.json"
OUTPUT_DIR = "data/teams_summary"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 브라우저 초기화
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 창 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# 나무위키 본문 추출 함수
def get_page_text(driver, url):
    try:
        driver.get(url)
        time.sleep(2.5)  # 렌더링 대기
        content = driver.find_element(By.TAG_NAME, "body").text
        return content
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return ""

# 메인 실행
def main():
    driver = init_driver()

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        team_links = json.load(f)

    for team_name, urls in team_links.items():
        print(f"📄 {team_name} 처리 중...")

        # 미러 주소 사용
        team_url = urls.get("team_url", "").replace("namu.wiki", "namu.moe")
        manager_url = urls.get("manager_url", "").replace("namu.wiki", "namu.moe")

        # 팀 및 감독 본문 추출
        team_text = get_page_text(driver, team_url)
        manager_text = get_page_text(driver, manager_url)

        # 최종 본문 구성
        combined_text = f"[팀 정보]\n{team_text.strip()}\n\n[감독 정보]\n{manager_text.strip()}"

        # 저장
        output_file = os.path.join(OUTPUT_DIR, f"{team_name}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(combined_text)

        print(f"✅ {team_name} 저장 완료")

    driver.quit()

if __name__ == "__main__":
    main()
