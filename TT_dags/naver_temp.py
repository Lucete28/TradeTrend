# temp = 기사제목
# raw = gpt ai
# base = 정제

# 기사 제목 받아오기
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import pandas as pd




# 현재 날짜 정보 가져오기
current_date = datetime.date.today()

# URL에 적용할 날짜 정보 포맷팅
year = current_date.year
month = current_date.month
day = current_date.day

# Chrome 웹 드라이버 옵션 설정
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 웹 창을 열지 않음
chrome_options.binary_location = '/usr/bin/google-chrome'  
# Chrome 웹 드라이버 초기화
driver = webdriver.Chrome(options=chrome_options)

l2 = []

url = f"https://search.naver.com/search.naver?where=news&query=삼성전자&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={year:04d}.{month:02d}.{day:02d}&de={year:04d}.{month:02d}.{day:02d}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{year:04d}{month:02d}{day:02d}to{year:04d}{month:02d}{day:02d}&is_sug_officeid=0"

driver.get(url)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

# articles = soup.select('#main_pack > section > div > div.group_news > ul > li')
# # print(articles)
# for article in articles:
#     a_tag = article.select_one('div.news_wrap.api_ani_send > div > a')
#     if a_tag:
#         title = a_tag.text
#         l2.append(title)

# driver.quit()

df =pd.DataFrame(l2)
df.to_csv("naver_TEMP.csv",index=False)