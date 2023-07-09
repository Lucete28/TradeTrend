from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import pendulum
from datetime import datetime, timedelta


local_tz = pendulum.timezone("Asia/Seoul")
default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime(year=2023, month=6, day=10, hour=0, minute=0, tzinfo=local_tz),
    'retries': 0,
    'retry_delay': timedelta(seconds=5)
}
test_dag = DAG(
    'TRB',
    schedule_interval = '0 23 * * *',
    user_defined_macros={'local_dt': lambda execution_date: execution_date.in_timezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")},
    # user_defined_macros={'local_dt': lambda ds: ds.in_timezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")},
    default_args = default_args
)


def gen_bash(task_id, bash_command, trigger_rule='all_success'):
    return BashOperator(
        task_id=task_id,
        bash_command=bash_command,
        trigger_rule=trigger_rule,
        dag=test_dag
    )

P_CODE = '/home/jhy/code/TradeTrend/TT_runfile/spark_p'
SH_PYSPARK = f'sh {P_CODE}/pyspark_submit.sh'
# P_PY_CODE = f'{P_CODE}/src/pyspark/tom'
EXE_SEOUL = "{{execution_date.add(hours=9).strftime('%Y%m%d')}}"
# DATA_SAMPLE_FRACTION = Variable.get('DATA_SAMPLE_FRACTION', default_var='')


def gen_spark(name: str):
    cmd = f"{SH_PYSPARK} {P_CODE}/{name}.py jhy_{name} {EXE_SEOUL}"
    return gen_bash(f"spark.{name}", cmd)


naver_temp = gen_bash(task_id='naver_temp', bash_command='python /mnt/c/PlayData/finance/news_temp.py {{execution_date.strftime("%Y-%m-%d")}}')
update_raw = gen_bash(task_id='update_raw', bash_command='python /home/jhy/code/TradeTrend/TT_runfile/update_naver_raw.py')

# fdr_spark = gen_spark(name='fdr_item')

fdr_data = gen_bash(task_id='fdr_data', bash_command='python /home/jhy/code/TradeTrend/TT_runfile/fdr_item_data.py')
ml = gen_bash(task_id='ml', bash_command='python /home/jhy/code/TradeTrend/TT_runfile/ml.py')
# trading = gen_bash(task_id='trading', bash_command='python /home/jhy/code/TradeTrend/TT_runfile/trading.py')

naver_temp >> update_raw >> fdr_data >> ml 



