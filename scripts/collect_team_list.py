import json
import os

# 리그별 팀 목록 (2025년 기준, 수동으로 입력)
k1_teams = [
    "울산 HD FC", "포항 스틸러스", "FC 서울", "대구 FC", "FC 안양",
    "전북 현대 모터스", "광주 FC", "대전 하나 시티즌", "제주 SK FC",
    "강원 FC", "수원 FC", "김천 상무 FC"
]

k2_teams = [
    "부산 아이파크", "화성 FC", "성남 FC", "천안 시티 FC", "전남 드래곤즈", "수원 삼성 블루윙즈", "인천 유나이티드 FC",
    "안산 그리너스 FC", "충북 청주 FC", "서울 이랜드 FC", "김포 FC", "경남 FC", "부천 FC 1995", "충남 아산 FC"
]

k3_teams = [
    "포천시민축구단", "울산시민축구단", "강릉시민축구단", "경주 한국수력원자력 축구단", "김해 FC 2008", "대전 코레일 FC", "시흥시민축구단",
    "창원 FC", "여주 FC", "파주시민축구단", "춘천시민축구단", "FC 목포", "부산교통공사 축구단", "양평 FC", "전북 현대 모터스 N"
]

output_path = "data/teams"
os.makedirs(output_path, exist_ok=True)

def save_teams(filename, data):
    with open(os.path.join(output_path, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_teams("k1_teams.json", k1_teams)
save_teams("k2_teams.json", k2_teams)
save_teams("k3_teams.json", k3_teams)

print("✅ 팀 목록 저장 완료")
