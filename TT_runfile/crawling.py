# 오후 11시에 그날 뉴스기사 받기
from airflow.models.variable import Variable
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import FinanceDataReader as fdr
import sys
import os

Target_list = Variable.get("Target_list")
values = [tuple(item.strip("()").split(",")) for item in Target_list.split("),")]
values = [(x[0].strip(), x[1].strip()) for x in values]

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
    try:
        old_df = pd.read_csv(f'/opt/airflow/src/{val[0]}/{val[0]}_temp4.csv')
    except:
        os.makedirs(f'/opt/airflow/src/{val[0]}')
        columns = ['0','1']
        old_df= pd.DataFrame(columns=columns)

    val_li = []

    # 날짜 설정
    execution_date = sys.argv[1]
    today_year = execution_date[:4]
    today_month = execution_date[5:7]
    today_day = execution_date[8:10]

    try:
        start_date = old_df.iloc[-1, 0]
    except:
        start_date = "2020-01-01"

    date_list = get_date_range(start_date, execution_date)

    for target_date in date_list:
        fdr_df = fdr.DataReader(val[0], '2020')
        fdr_df_date = fdr_df.index.tolist()
        formatted_dates = [date.strftime('%Y-%m-%d') for date in fdr_df_date]

        today_year = target_date[:4]
        today_month = target_date[5:7]
        today_day = target_date[8:10]

        if target_date in formatted_dates: # 주식 장이 열렸던 날이고
            if target_date not in old_df.iloc[:, 0].tolist():# 기사가 적재되어있지 않으면
                l2 = []
                url = f"https://search.naver.com/search.naver?where=news&query={val[1]}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={int(today_year):04d}.{int(today_month):02d}.{int(today_day):02d}&de={int(today_year):04d}.{int(today_month):02d}.{int(today_day):02d}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{int(today_year):04d}{int(today_month):02d}{int(today_day):02d}to{int(today_year):04d}{int(today_month):02d}{int(today_day):02d}&is_sug_officeid=0"

                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.select('#main_pack > section > div > div.group_news > ul > li')

                for article in articles:
                    a_tag = article.select_one('div.news_wrap.api_ani_send > div > a')
                    if a_tag:
                        title = a_tag.text
                        l2.append(title)
    
                new_row = [target_date, [l2]]
                old_df.loc[len(old_df)] = new_row
                old_df = pd.DataFrame(old_df)
                old_df.to_csv(f'/opt/airflow/src/{val[0]}/{val[0]}_temp4.csv', index=False)
                    
                # raw df update
                
                raw_df = pd.read_csv(f'/opt/airflow/src/{val[0]}/{val[0]}_news_raw2.csv')
                raw_df.loc[len(raw_df)] = new_row
                raw_df.to_csv(f'/opt/airflow/src/{val[0]}/{val[0]}_news_raw2.csv', index=False)
print('##################################')

