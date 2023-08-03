import datetime
import pandas as pd
import FinanceDataReader as fdr
import requests
from bs4 import BeautifulSoup

values = ["삼성전자"]


def get_date_range(start_date, end_date):
    date_range = []
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    delta = datetime.timedelta(days=1)
    
    while start <= end:
        date_range.append(start.strftime("%Y-%m-%d"))
        start += delta
    
    return date_range

for val in values:

        
    val_li = []
    
    # 날짜 설정
    execution_date = "2023-07-25"
    today_year = execution_date[:4]
    today_month = execution_date[5:7]
    today_day = execution_date[8:10]


    target_date= execution_date
   
    fdr_df = fdr.DataReader(val[0], '2020')
    fdr_df_date = fdr_df.index.tolist()


    today_year = target_date[:4]
    today_month = target_date[5:7]
    today_day = target_date[8:10]



    l2=[]
    url = f"https://search.naver.com/search.naver?where=news&query={val}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={int(today_year):04d}.{int(today_month):02d}.{int(today_day):02d}&de={int(today_year):04d}.{int(today_month):02d}.{int(today_day):02d}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{int(today_year):04d}{int(today_month):02d}{int(today_day):02d}to{int(today_year):04d}{int(today_month):02d}{int(today_day):02d}&is_sug_officeid=0"
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    articles = soup.select('#main_pack > section > div > div.group_news > ul > li')
    
    for article in articles:
        a_tag = article.select_one('div.news_wrap.api_ani_send > div > a')
        if a_tag:
            title = a_tag.text
            l2.append(title)
c =0  

for i in l2:
    c+=1
    print(c,i)

print('##################################')

