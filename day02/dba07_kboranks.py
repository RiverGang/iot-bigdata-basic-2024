from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# 웹 드라이버 설정 (여기서는 ChromeDriver 사용 예시)
driver_path = 'path_to_chromedriver'  # Chromedriver 경로 지정
driver = webdriver.Chrome(driver_path)

# 수집할 날짜 리스트 생성 (예시: 2024년 3월 23일부터 2024년 7월 24일까지)
dates = pd.date_range(start="2024-03-23", end="2024-07-24").strftime('%Y-%m-%d')

# 데이터를 저장할 빈 리스트 초기화
all_data = []

# 기본 URL 설정
url = 'https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx'

for date in dates:
    # 페이지 로드
    driver.get(url)
    time.sleep(2)  # 페이지가 로드될 시간을 주기 위해 대기

    # 날짜 선택 드롭다운 메뉴 조작 (예: 여기선 없는 상황을 가정하고, 단순히 페이지에서 데이터 추출)
    # 실제로는 이 부분에서 각 날짜에 맞는 데이터를 선택하도록 처리 필요

    # 테이블 데이터 추출
    table = driver.find_element(By.CLASS_NAME, 'tData')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # 첫 번째 행에서 컬럼명 추출 (첫날만 필요)
    if not all_data:
        columns = ["날짜"] + [header.text for header in rows[0].find_elements(By.TAG_NAME, 'th')]

    # 데이터 행 추출
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [date] + [cell.text for cell in cells]
        all_data.append(row_data)

# 웹 드라이버 종료
driver.quit()

# DataFrame으로 변환
df = pd.DataFrame(all_data, columns=columns)

# 엑셀 파일로 저장
df.to_excel('KBO_team_rankings_by_date.xlsx', index=False)

print("Data has been saved to KBO_team_rankings_by_date.xlsx")