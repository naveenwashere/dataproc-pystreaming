from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.dataproc_operator import DataProcPySparkOperator

yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': yesterday,
    'email': ['email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG('pi_dag_v0.5', schedule_interval='@once',
         default_args=default_args) as dag:

    create_cluster = BashOperator(
        task_id='setup_cluster',
        bash_command='gcloud dataproc clusters create sample-cluster '
                     + '--master-boot-disk-size=20GB --master-machine-type=n1-standard-1 '
                     + '--num-masters=1 --num-workers=2 --quiet',
        execution_timeout=timedelta(minutes=15)
    )

    dataproc_pyspark_submit = DataProcPySparkOperator(
        task_id='pi_task',
        main='gs://fico-spark-jobs/spark/pi.py',
        job_name='dataproc_pi_job',
        cluster_name='sample-cluster'
    )

    delete_cluster = BashOperator(
        task_id='delete_cluster',
        bash_command='gcloud dataproc clusters delete sample-cluster --quiet',
        execution_timeout=timedelta(minutes=15)
    )

create_cluster >> dataproc_pyspark_submit >> delete_cluster