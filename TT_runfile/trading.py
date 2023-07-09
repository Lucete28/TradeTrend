from airflow.models.variable import Variable
import pandas as pd 
import mojito
import pprint

key = Variable.get("TT_api_key")
secret = Variable.get("TT_api_secret_key")
acc_no = Variable.get("TT_acc_no")

Target_list  =  Variable.get("Target_list")
values = [tuple(item.strip("()").split(",")) for item in Target_list.split("),")]
values = [(x[0].strip(), x[1].strip()) for x in values]

broker = mojito.KoreaInvestment(
    api_key = key,
    api_secret = secret,
    acc_no = acc_no,
    mock = True #만약 모의투자면 이 항목 True로 설정
)

receipt = []
resp = broker.fetch_balance()
asst_icdc_amt = resp['output2'][0]['asst_icdc_amt'] #장내 현금 보유액



for val in values: 
    result_df = pd.read_csv(f'/home/jhy/code/TradeTrend/data/{val[0]}_result.csv')
    # acc7_df = pd.read_csv('/home/jhy/code/TradeTrend/data/Accuracy_7.csv')
    # acc30_df = pd.read_csv('/home/jhy/code/TradeTrend/data/Accuracy_30.csv')

    negative_count = len(result_df[result_df.iloc[:,-1] < 0])
    positive_count = len(result_df[result_df.iloc[:,-1] > 0])

    if positive_count>negative_count:     #'구매 or 존버'
        if True: #구매
            resp = broker.create_market_buy_order(
            symbol= val[0],
            quantity=10
            )
            receipt.append(resp)
            
    elif negative_count > positive_count: #'판매 or 안구매'
        if True: #판매
            resp = broker.fetch_balance()
            hldg_qty = resp['output1'][0]['hldg_qty']
            resp = broker.create_market_sell_order(
            symbol= val[0],
            quantity=hldg_qty
            )
            receipt.append(resp)












result_df = pd.DataFrame({'Count': [result_negative_count, result_positive_count]},
                         index=['Negative', 'Positive'])


result_df.to_csv('/home/jhy/code/TradeTrend/data/negative_positive_count.csv')