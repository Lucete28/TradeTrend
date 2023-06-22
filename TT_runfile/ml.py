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
    
df = pd.read_csv('/home/jhy/code/TradeTrend/data/005930_temp.csv')
df = df.drop(['Date','Volume_USD/KRW'],axis=1)

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
            new_df = df.iloc[:-i]
            y_train = new_df.loc[1:,target]
            X_train = new_df.iloc[:-1]
            x_test = new_df.iloc[-1:]
            y_test = df.iloc[-i][target]
            model.fit(X_train, y_train)
            predictions = model.predict(x_test)
            check.append((get_sign(predictions[0][-1]),get_sign(y_test[-1])))
        else:
            new_df=df
            y_train = new_df.loc[1:,target]
            X_train = new_df.iloc[:-1]
            x_test = new_df.iloc[-1:]
            
            model.fit(X_train, y_train)
            predictions = model.predict(x_test)
            tmp_list.append(predictions[0].tolist())
    
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
        'Rise_pred Accuracy': (rise_real_count_7 / rise_pred_count_7) * 100 if rise_pred_count_7 != 0 else 'N/A (pred_count가 0입니다)',
        'Fall_pred Accuracy': (fall_real_count_7 / fall_pred_count_7) * 100 if fall_pred_count_7 != 0 else 'N/A (pred_count가 0입니다)',
    }
    Accuracy_7.append(result_dict_7)
    df_acc_7 = pd.DataFrame(Accuracy_7)
    df_acc_7.to_csv('/home/jhy/code/TradeTrend/data/Accuracy_7.csv',index=False)
    
    result_dict_30 = {
        'Model Name': type(model.estimator).__name__,
        'real_rise' : real_rise_count_30,
        'rise_pred_count' : rise_pred_count_30,
        'real_fall' : real_fall_count_30,
        'fall_pred_count' : fall_pred_count_30,
        'Rise_pred Accuracy': (rise_real_count_30 / rise_pred_count_30) * 100 if rise_pred_count_30 != 0 else 'N/A (pred_count가 0입니다)',
        'Fall_pred Accuracy': (fall_real_count_30 / fall_pred_count_30) * 100 if fall_pred_count_30 != 0 else 'N/A (pred_count가 0입니다)',
    }
    Accuracy_30.append(result_dict_30)
    df_acc_30 = pd.DataFrame(Accuracy_30)
    df_acc_30.to_csv('/home/jhy/code/TradeTrend/data/Accuracy_30.csv',index=False)

pd.DataFrame(result_list,index=model_names,columns=target).to_csv('/home/jhy/code/TradeTrend/data/result.csv')
