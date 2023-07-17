### 최근 n 회 분석해서 예측 성공률 분석
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pandas as pd 
from lightgbm import LGBMRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import xgboost as xgb
from airflow.models.variable import Variable
Target_list  =  Variable.get("Target_list")
values = [tuple(item.strip("()").split(",")) for item in Target_list.split("),")]
values = [(x[0].strip(), x[1].strip()) for x in values]

def unscale_row(row, column_ranges):
    unscaled_row = {}
    for i, column in enumerate(column_ranges):
        value = row[i]
        min_val = column_ranges[column]['min']
        max_val = column_ranges[column]['max']
        unscaled_val = (value * (max_val - min_val)) + min_val
        unscaled_row[column] = unscaled_val
    return pd.Series(unscaled_row)

for val in values:
    lin_model = MultiOutputRegressor(LinearRegression())
    lgbm_model = MultiOutputRegressor(LGBMRegressor())
    random_forest_model = MultiOutputRegressor(RandomForestRegressor())
    knn_model = MultiOutputRegressor(KNeighborsRegressor())
    decision_tree_model = MultiOutputRegressor(DecisionTreeRegressor())
    gradient_boosting_model = MultiOutputRegressor(GradientBoostingRegressor())
    xgboost_model = MultiOutputRegressor(xgb.XGBRegressor())

    def get_sign(a):
        if a == 'nan':
            return 2
        elif a < 0:
            return -1
        elif a == 0:
            return 0
        else:
            return 1
    
    df = pd.read_csv(f'/home/jhy/code/TradeTrend/data/{val[0]}/{val[0]}_temp.csv')
    df = df.drop(['Date','Volume_USD/KRW'],axis=1)
    df = df.iloc[:-1]
    scaled_df = df
    column_ranges = {}

    # 각 열별로 min-max 스케일링 수행
    # scaled_df = pd.DataFrame()
    # for column in df.columns:
    #     # 최솟값과 최댓값 기록
    #     min_val = df[column].min()
    #     max_val = df[column].max()
    #     column_ranges[column] = {'min': min_val, 'max': max_val}
        
    #     # min-max 스케일링
    #     scaled_vals = (df[column] - min_val) / (max_val - min_val)
    #     scaled_df[column] = scaled_vals
    # column_ranges_2 = {}
    # for i in ['Open','High','Low','Close','Volume','Change']:
    #     if i in column_ranges:
    #         column_ranges_2[i] = column_ranges[i]
    # column_ranges = column_ranges_2
    
    Accuracy_list = []
    Accuracy_7 = []
    Accuracy_30 = []
    result_list = []
    models = [lin_model, lgbm_model, random_forest_model, knn_model, decision_tree_model, gradient_boosting_model,xgboost_model]
    model_names = []
    target  = ['Open', 'High', 'Low', 'Close', 'Volume', 'Change']
    for model in models:
        model_names.append(type(model.estimator).__name__)
        print(type(model.estimator).__name__)
        tmp_list = []
        check= []
        for i in range(31):
            if i !=0:
                new_df = scaled_df.iloc[:-i]
                y_train = new_df.loc[1:,target]
                X_train = new_df.iloc[:-1]
                x_test = new_df.iloc[-1:]
                y_test = scaled_df.iloc[-i][target]
                model.fit(X_train, y_train)
                predictions = model.predict(x_test)
                check.append((get_sign(predictions[0][-1]),get_sign(y_test[-1])))
            else:
                new_df=scaled_df
                y_train = new_df.loc[1:,target]
                X_train = new_df.iloc[:-1]
                x_test = new_df.iloc[-1:]
                
                model.fit(X_train, y_train)
                predictions = model.predict(x_test)
                tmp_list.append(predictions[0].tolist())
        # result_list.append(unscale_row(tmp_list[0], column_ranges))
        result_list.append(tmp_list[0])
        ########################################################################################
    # tmp_count_list = [(check[:7]),(check)]
    # for j,k in enumerate(tmp_count_list):
        
        rise_real_count_7 = 0
        rise_pred_count_7 = 0
        fall_real_count_7 = 0
        fall_pred_count_7 = 0
        real_rise_count_7 = 0
        real_fall_count_7 = 0
        
        rise_real_count_30 = 0
        rise_pred_count_30 = 0
        fall_real_count_30 = 0
        fall_pred_count_30 = 0
        real_rise_count_30 = 0
        real_fall_count_30 = 0
        
        for j, i in enumerate(check):
            if j<=7:
                if i[0] == 1:
                    rise_pred_count_7 += 1
                    rise_pred_count_30 += 1
                    if i[1] == 1:
                        rise_real_count_7 += 1
                        rise_real_count_30 += 1
                elif i[0] == -1:
                    fall_pred_count_7 += 1
                    fall_pred_count_30 += 1
                    if i[1] == -1:
                        fall_real_count_7 += 1
                        fall_real_count_30 += 1
                if i[1] == 1:
                    real_rise_count_7+=1
                    real_rise_count_30+=1
                elif i[1] == -1:
                    real_fall_count_7+=1
                    real_fall_count_30+=1
            else: 
                if i[0] == 1:
                    rise_pred_count_30 += 1
                    if i[1] == 1:
                        rise_real_count_30 += 1
                elif i[0] == -1:
                    fall_pred_count_30 += 1
                    if i[1] == -1:
                        fall_real_count_30 += 1
                if i[1] == 1:
                    real_rise_count_30+=1
                elif i[1] == -1:
                    real_fall_count_30+=1
                


        result_dict_7 = {
            'Model Name': type(model.estimator).__name__,
            'real_rise' : real_rise_count_7,
            'rise_pred_count' : rise_pred_count_7,
            'real_fall' : real_fall_count_7,
            'fall_pred_count' : fall_pred_count_7,
            'Rise_pred Accuracy': (rise_real_count_7 / rise_pred_count_7) * 100 if rise_pred_count_7 != 0 else 0,
            'Fall_pred Accuracy': (fall_real_count_7 / fall_pred_count_7) * 100 if fall_pred_count_7 != 0 else 0,
        }
        Accuracy_7.append(result_dict_7)
        df_acc_7 = pd.DataFrame(Accuracy_7)
        df_acc_7.to_csv(f'/home/jhy/code/TradeTrend/data/{val[0]}/{val[0]}_Accuracy_7.csv',index=False)
        
        result_dict_30 = {
            'Model Name': type(model.estimator).__name__,
            'real_rise' : real_rise_count_30,
            'rise_pred_count' : rise_pred_count_30,
            'real_fall' : real_fall_count_30,
            'fall_pred_count' : fall_pred_count_30,
            'Rise_pred Accuracy': (rise_real_count_30 / rise_pred_count_30) * 100 if rise_pred_count_30 != 0 else 0,
            'Fall_pred Accuracy': (fall_real_count_30 / fall_pred_count_30) * 100 if fall_pred_count_30 != 0 else 0,
        }
        Accuracy_30.append(result_dict_30)
        df_acc_30 = pd.DataFrame(Accuracy_30)
        df_acc_30.to_csv(f'/home/jhy/code/TradeTrend/data/{val[0]}/{val[0]}_Accuracy_30.csv',index=False)

    pd.DataFrame(result_list,index=model_names,columns=target).to_csv(f'/home/jhy/code/TradeTrend/data/{val[0]}/{val[0]}_result.csv')
