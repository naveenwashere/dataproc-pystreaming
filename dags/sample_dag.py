from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': yesterday,
    'email': ['naveenwashere@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

with DAG('v1_8_dataproc', schedule_interval=timedelta(days=1),
         default_args=default_args) as dag:

    no_run = DummyOperator(task_id='no_run')

    no_run
