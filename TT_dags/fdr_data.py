import FinanceDataReader as fdr

name_list = ['005930']
for name in name_list:
    df = fdr.DataReader(name, '2020')
    df.iloc[-1,:]