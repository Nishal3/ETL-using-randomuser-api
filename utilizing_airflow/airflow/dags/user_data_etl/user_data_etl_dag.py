from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

sys.path.insert(1, "/home/ubuntu/ETL-using-randomuser-api/utilizing_airflow/")
from raw_data_fetcher import data_fetcher
from data_cleaner import clean_data
from producer_node import produce_data
from consumer_node import consume_data

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

data_fetching = PythonOperator(
        task_id="data_fetching_task", python_callable=data_fetcher, dag=dag
)

data_parsing = PythonOperator(
        task_id="data_parsing_task", python_callable=clean_data, dag=dag
)

production_task = PythonOperator(
    task_id="production_task", python_callable=produce_data, dag=dag
)

consumption_task = PythonOperator(
    task_id="consumption_task", python_callable=consume_data, dag=dag
)


data_fetching >> data_parsing
data_parsing >> production_task
production_task >> consumption_task
