# 종목, 종목기사, 공통 데이터를 불러와서 temp, raw 만들어 제공
# temp : 그냥 머지앤 클린
# raw : mm scaling

### 뉴스 df가 하나뿐임 수정 필요
### 공통 데이터 추가 목표

import FinanceDataReader as fdr
import pandas as pd 
from airflow.models.variable import Variable

target_list  =  Variable.get("Target_list").split(",")

def merge_and_clean(df1,df1_name,df2,df2_name):
    merged_df = df1.join(df2, how='outer', lsuffix=df1_name, rsuffix=df2_name)
    df = merged_df.dropna()
    return df

def min_max_scaling(df):
    scaled_df = df.copy()
    for col in df.columns[1:]:
        min_val = df[col].min()
        max_val = df[col].max()
        scaled_df[col] = (df[col] - min_val) / (max_val - min_val)
    return scaled_df

df1 = fdr.DataReader('USD/KRW', '2020')
df2 = fdr.DataReader('ks11', '2020')

news_df = pd.read_csv('/home/jhy/code/TradeTrend/data/news_raw2.csv', index_col=0)  # 첫 번째 열을 인덱스로 설정
common_df = merge_and_clean(df1,'_USD/KRW',df2,'_ks11')
news_df.index = pd.to_datetime(news_df.index)

for target in target_list:
    df = fdr.DataReader(target, '2020')
    target_df = merge_and_clean(df,target,news_df,'news')
    
    final_df = merge_and_clean(target_df,target,common_df,'_common')
    final_df.reset_index().to_csv(f'/home/jhy/code/TradeTrend/data/{target}_temp.csv')
    sc_df = min_max_scaling(final_df)
    sc_df.reset_index().to_csv(f'/home/jhy/code/TradeTrend/data/{target}_raw.csv')
    print(sc_df.shape)
    print('#####################################################################')



