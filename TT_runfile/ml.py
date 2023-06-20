### 최근 n 회 분석해서 예측 성공률 분석
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pandas as pd 
from lightgbm import LGBMRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
import json

df = pd.read_csv('/home/jhy/code/TradeTrend/data/005930_temp.csv')
df = df.drop(['Date','Volume_USD/KRW'],axis=1)

def get_sign(a):
    if a < 0:
        return -1
    elif a == 0:
        return 0
    else:
        return 1
lin_model = MultiOutputRegressor(LinearRegression())
lgbm_model = MultiOutputRegressor(LGBMRegressor())
random_forest_model = MultiOutputRegressor(RandomForestRegressor())
knn_model = MultiOutputRegressor(KNeighborsRegressor())
decision_tree_model = MultiOutputRegressor(DecisionTreeRegressor())
gradient_boosting_model = MultiOutputRegressor(GradientBoostingRegressor())
result_list = []

models = [lin_model, lgbm_model, random_forest_model, knn_model, decision_tree_model, gradient_boosting_model]
model_names = [ ]
for model in models:
    check= []
    for i in range(1,11):
        new_df = df.iloc[:-i]
        y_train = new_df.loc[1:,['Open','High','Low','Close','Volume','Change']]
        X_train = new_df.iloc[:-1]
        x_test = new_df.iloc[-1:]
        y_test = df.iloc[-i][['Open', 'High', 'Low', 'Close', 'Volume', 'Change']]

        model.fit(X_train, y_train)
        predictions = model.predict(x_test)

        check.append((get_sign(predictions[0][-1]),get_sign(y_test[-1])))

    
    rise_real_count = 0
    rise_pred_count = 0
    fall_real_count = 0
    fall_pred_count = 0

    for i in check:
        if i[0] == 1:
            rise_pred_count += 1
            if i[1] == 1:
                rise_real_count += 1
        elif i[0] == -1:
            fall_pred_count += 1
            if i[1] == -1:
                fall_real_count += 1

    if rise_pred_count != 0:
        rise_accuracy = (rise_real_count / rise_pred_count) * 100
        result_list.append(f"{type(model.estimator).__name__} 상승 적중률: {rise_accuracy}%")
    else:
        result_list.append(f"{type(model.estimator).__name__} 상승 적중률: N/A (pred_count가 0입니다)")

    if fall_pred_count != 0:
        fall_accuracy = (fall_real_count / fall_pred_count) * 100
        result_list.append(f"{type(model.estimator).__name__} 하강 적중률: {fall_accuracy}%")
    else:
        result_list.append(f"{type(model.estimator).__name__} 하강 적중률: N/A (pred_count가 0입니다)")

file_path = '/home/jhy/code/TradeTrend/data/result.txt'

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(result_list, file, ensure_ascii=False)