import pandas as pd

df = pd.DataFrame(columns=['date', 'naver_news'], index=[0])
df.to_csv('news_temp.csv',index=False)