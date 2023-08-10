from airflow.exceptions import AirflowException
from airflow.models.variable import Variable
import openai
import pandas as pd

openai.api_key = Variable.get("gpt_api_key")
Target_list = Variable.get("Target_list")
values = [tuple(item.strip("()").split(",")) for item in Target_list.split("),")]
values = [(x[0].strip(), x[1].strip()) for x in values]

err_report = []
error_count = {}  # 오류 카운트를 추적하기 위한 딕셔너리

for val in values:
    gpt_ans = []

    temp_df = pd.read_csv(f'/opt/airflow/src/{val[0]}/{val[0]}_temp4.csv')
    raw_df = pd.read_csv(f'/opt/airflow/src/{val[0]}/{val[0]}_news_raw2.csv')

    ans_list = raw_df.iloc[:, 1]
    while True:
        condition_satisfied = True

        for i, ans in enumerate(ans_list):
            try:
                if len(str(ans)) > 4 or (float(ans) > 1 or float(ans) < 0):
                    messages = []
                    a = temp_df.iloc[i, 1]
                    content = f'{a} {val[1]} 관련 뉴스기사 제목인데 {val[1]} 주식에 미칠 긍정도의 평균을 0에서 1사이 소숫점 두자리까지 나타내 float값만'
                    messages.append({"role": "user", "content": content})

                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )

                    chat_response = completion.choices[0].message.content
                    gpt_ans.append(chat_response)
                    messages.append({"role": "assistant", "content": chat_response})

                    raw_df.iloc[i, 1] = chat_response
                    raw_df.to_csv(f'/opt/airflow/src/{val[0]}/{val[0]}_news_raw2.csv', index=False)

                    condition_satisfied = False
            except Exception as e:
                print(i, ans)
                err_report.append(ans)
                condition_satisfied = False
                error_count[ans] = error_count.get(ans, 0) + 1

        for err, count in error_count.items():
            if count >= 5:
                raise AirflowException(f"{val[0]}에서 에러 '{err}'가 5회 이상 발생하여 작업을 종료합니다.")

        if condition_satisfied:
            break

