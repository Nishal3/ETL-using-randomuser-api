from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys


sys.path.insert(1, "/home/ubuntu/ETL-using-randomuser-api/")
from random_data_gen_consumer import consume_data as consumer
from random_data_gen_producer import production_scheduler as producer

default_args = {
    "owner": "Nishal",
    "depends_on_past": False,
    "start_date": datetime.now(),
    "email": ['nepalnishal4@gmail.com'],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "user_data_dag",
    default_args=default_args,
    description="user_data_dag",
    schedule=None
)

production_task = PythonOperator(
    task_id="production_task", python_callable=producer, dag=dag
)

consumption_task = PythonOperator(
    task_id="consumption_task", python_callable=consumer, dag=dag
)

production_task >> consumption_task
