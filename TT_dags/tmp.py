from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from time import sleep

# DAG 기본 인수 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 생성
dag = DAG(
    'example_dag',
    default_args=default_args,
    description='An example DAG',
    schedule_interval=timedelta(days=1),  # 원하는 스케줄링 간격 설정
)

# PythonOperator로 실행될 함수 정의
def print_hello():
    return 'Hello, Airflow!'

# PythonOperator로 실행될 함수 정의 (5초 동안 sleep)
def sleep_task():
    sleep(5)
    return 'Sleep task complete!'

# PythonOperator로 실행되는 함수를 실행할 작업 정의
print_hello_task = PythonOperator(
    task_id='print_hello_task',
    python_callable=print_hello,
    dag=dag,
)

sleep_task = PythonOperator(
    task_id='sleep_task',
    python_callable=sleep_task,
    dag=dag,
)

# Task 간의 순서 설정
print_hello_task >> sleep_task

