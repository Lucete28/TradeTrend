# 전날 뉴스 기사를 받아옴
from airflow.models.variable import Variable
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import pandas as pd
import FinanceDataReader as fdr
import sys

a = Variable.get("Target_list")
values = [tuple(item.strip("()").split(",")) for item in a.split("),")]
values = [(x[0].strip(), x[1].strip()) for x in values]
print(values)
print(values[0][0])
fdr_df = fdr.DataReader(values[0][0], '2020')
print(fdr_df.head(1))