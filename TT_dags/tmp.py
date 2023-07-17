# 전날 뉴스 기사를 받아옴
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import pandas as pd
import FinanceDataReader as fdr
import sys

# 날짜 설정
execution_date = sys.argv[1]
yesterday_stamp= pd.Timestamp(execution_date) + pd.Timedelta(days=-1)
str_date = str(yesterday_stamp)
yesterday = str_date[:10]
yesterday_year = str_date[:4]
yesterday_month = str_date[5:7]
yesterday_day = str_date[8:10]

print(yesterday_day)
print('###############################')
