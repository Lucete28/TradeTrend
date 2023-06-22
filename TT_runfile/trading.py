from airflow.models.variable import Variable
import pandas as pd 

result_df = pd.read_csv('/home/jhy/code/TradeTrend/data/result.csv')
# acc7_df = pd.read_csv('/home/jhy/code/TradeTrend/data/Accuracy_7.csv')
# acc30_df = pd.read_csv('/home/jhy/code/TradeTrend/data/Accuracy_30.csv')

result_negative_count = len(result_df[result_df.iloc[:,-1] < 0])
result_positive_count = len(result_df[result_df.iloc[:,-1] > 0])

if result_positive_count>result_negative_count:
    '구매 or 존버'
elif result_negative_count > result_positive_count:
    '판매 or 안구매'













result_df = pd.DataFrame({'Count': [result_negative_count, result_positive_count]},
                         index=['Negative', 'Positive'])


result_df.to_csv('/home/jhy/code/TradeTrend/data/negative_positive_count.csv')