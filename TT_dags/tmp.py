from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import pendulum
from datetime import datetime, timedelta
from airflow.models.variable import Variable

local_tz = pendulum.timezone("Asia/Seoul")
target_list  =  (Variable.get("Target_list")).split(",")
print(type(target_list))

print(target_list)
# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': True,
#     'start_date': datetime(year=2023, month=6, day=10, hour=0, minute=0, tzinfo=local_tz),
#     'retries': 10,
#     'retry_delay': timedelta(seconds=5)
# }
# test_dag = DAG(
#     'TRB',
#     schedule_interval = '0 23 * * *',
#     user_defined_macros={'local_dt': lambda execution_date: execution_date.in_timezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")},
#     # user_defined_macros={'local_dt': lambda ds: ds.in_timezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")},
#     default_args = default_args
# )


# def gen_bash(task_id, bash_command, trigger_rule='all_success'):
#     return BashOperator(
#         task_id=task_id,
#         bash_command=bash_command,
#         trigger_rule=trigger_rule,
#         dag=test_dag
#     )


# naver_temp = gen_bash(task_id='naver_temp', bash_command='echo target_list')