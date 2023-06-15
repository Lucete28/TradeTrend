import FinanceDataReader as fdr
import pandas as pd 

def min_max_scaling(df):
    scaled_df = df.copy()
    for col in df.columns[1:]:
        min_val = df[col].min()
        max_val = df[col].max()
        scaled_df[col] = (df[col] - min_val) / (max_val - min_val)
    return scaled_df

name_list = ['005930']
for name in name_list:
    df = fdr.DataReader(name, '2020')
    df.reset_index().to_csv(f"/home/jhy/code/TradeTrend/data/{name}_temp.csv", index=False)

    df = pd.read_csv(f'/home/jhy/code/TradeTrend/data/{name}_temp.csv')
    raw_df = min_max_scaling(df)
    raw_df.to_csv(f'/home/jhy/code/TradeTrend/data/{name}_raw.csv',index=False)
    
