from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Chrome 옵션 설정 (Headless 모드를 사용하지 않을 경우 주석 처리)
# options = Options()
# options.headless = True

# Chrome 드라이버 생성

# 크롬 드라이버의 전체 경로를 지정합니다.
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/google-chrome-stable"
chrome_options.add_argument("--headless")  # Headless 모드로 실행
driver = webdriver.Chrome(options=chrome_options)

try:
    # 웹 사이트 열기
    driver.get("https://www.google.com")  # 크롤링할 웹 사이트 주소를 입력합니다.
    
    # 페이지 로딩을 위해 잠시 대기 (2초)
    time.sleep(2)
    
    # 페이지 타이틀 출력
    print("페이지 타이틀:", driver.title)
    
    # 웹 사이트에서 필요한 작업을 수행합니다.
    # 여기에 크롤링하려는 웹 페이지의 요소에 접근하고 데이터를 수집하는 코드를 작성합니다.
    
finally:
    # 드라이버를 닫고 리소스를 정리합니다.
    driver.quit()

