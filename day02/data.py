from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Selenium 웹 드라이버 설정 (크롬 드라이버 사용)
chrome_options = Options()
driver = webdriver.Chrome()

# 사이트 접속
url = "https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx"
driver.get(url)

# 데이터가 로드될 때까지 대기
time.sleep(3)

# BeautifulSoup 사용하여 페이지 파싱
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 팀 순위 테이블 추출
table = soup.find('table', {'class': 'tData'})

# 테이블에서 데이터 추출
columns = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
data = []
for row in table.find('tbody').find_all('tr'):
    data.append([td.get_text(strip=True) for td in row.find_all('td')])

# 데이터프레임으로 변환
df = pd.DataFrame(data, columns=columns)

# 데이터 출력
print(df)

# 드라이버 종료
driver.quit()

# 결과를 CSV로 저장
df.to_csv('team_rank_daily.csv', index=False, encoding='utf-8-sig')