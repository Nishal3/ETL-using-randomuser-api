from airflow.decorators import dag, task
from airflow import macros
from confluent_kafka import Producer, Consumer
from sqlalchemy import create_engine, text
import sys
import random
import json
import requests
import time
import os
import logging

MODE = os.getenv("DEV")
HOME = os.getenv("HOME")
USERNAME = "postgres"
PASSWORD = None
IP = None

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)
logger = logging.getLogger("user_dag_logger")

file_handler = logging.FileHandler(HOME + "/airflow/dags/log/userd_log.log")

file_handler.setFormatter(
    logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
)

logger.addHandler(file_handler)

sys.path.insert(1, HOME + "/bin/de_projects/ETL-using-randomuser-api/")
# Configuration and functions needed to run tasks
from assistant_functions.data_cleaner_funcs import assemble_data
from assistant_functions.producer_node_funcs import production_loop
from config.config import config as main_config
from assistant_functions.consumer_node_funcs import (
    set_configs,
    assignment_callback,
    procure_data,
)

with open(
    HOME + "/bin/de_projects/ETL-using-randomuser-api/config/password.txt", "r"
) as password:
    file_input = password.readline()
    if file_input:
        PASSWORD = file_input.rstrip("\n")

with open(
    HOME + "/bin/de_projects/ETL-using-randomuser-api/config/ip_address.txt",
    "r",
) as ip_address:
    file_input = ip_address.readline()
    if file_input:
        IP = file_input.rstrip("\n")

with open(
    HOME + "/bin/de_projects/ETL-using-randomuser-api/config/username.txt", "r"
) as username:
    file_input = username.readline()
    if file_input:
        USERNAME = file_input.rstrip("\n")

default_args = {
    "owner": "Nishal",
    "start_date": macros.datetime.now(),
    "retries": 1,
    "retry_delay": macros.timedelta(minutes=5),
}


@dag(schedule="*/5 * * * *", default_args=default_args, catchup=False)
def userd_dag():
    def data_loader(data, db_url=None):
        table = list(data.keys())[0]
        data_keys = list(list(data.values())[0].keys())
        data_vals = list(list(data.values())[0].values())

        data_vals = ", ".join(
            [
                f'"{str(i)}"'
                if isinstance(i, int) or isinstance(i, str)
                else "ARRAY"
                + "["
                + ", ".join([f'"{str(j)}"' if j else f'"None"' for j in i])
                + "]"
                for i in data_vals
            ]
        )

        data_vals = data_vals.replace("'", "''")
        data_vals = data_vals.replace('"', "'")

        if MODE:
            print(f"Table: {table}, Columns: {data_keys}, Values: {data_vals}")
        if db_url is None:
            print("Please provide a database url")
            sys.exit(1)

        engine = create_engine(db_url, future=True)
        connection = engine.connect()
        print(f"Table: {table}, Columns: {data_keys}, Values: {data_vals}")
        connection.execute(
            text(f"INSERT INTO {table} ({', '.join(data_keys)}) VALUES ({data_vals})")
        )

        connection.commit()
        connection.close()

    @task
    def raw_data_fetcher(data_to_load=0, link="https://randomuser.me/api/"):
        if not data_to_load:
            data_to_load = random.randint(1, 150)
        final_output = []
        while data_to_load > 0:
            api = requests.get(link)
            cleaned = json.loads(api.text)["results"][0]
            final_output.append(cleaned)
            data_to_load -= 1
            time.sleep(0.01)

        if not final_output:
            logger.error("`final_output` has no value.")
            sys.exit(1)

        return final_output

    @task
    def data_cleaner(raw_data=None):
        if not raw_data:
            logger.error(f"`data` has no value.")
            sys.exit(1)

        results = []
        for i in raw_data:
            results.append(assemble_data(i))

        if not results:
            logger.error("`results` has no value")
            sys.exit(1)

        return results

    @task
    def producer_node(results):
        producer = Producer(main_config)
        logger.info("Producer Node running")
        for i in results:
            production_loop(producer, i)
            producer.flush()
        logger.info("Production looping finished")

    @task
    def consumer_node():
        config = set_configs()
        consumer = Consumer(config)
        consumer.subscribe(
            ["main", "login", "location", "identification", "image"],
            on_assign=assignment_callback,
        )

        logger.info("Consumer configs finished and ready to loop to consume")

        try:
            time_start = time.time()
            time_til_start = 0
            while time_til_start < 10:
                logging.info("Start of consuming loop")
                time_til_start = time.time() - time_start
                event = consumer.poll(1.0)
                if event is None:
                    continue
                else:
                    data_dict = procure_data(event)
                    logger.info(f"data collected")
                    url = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:5432/test"
                    data_loader(
                        data_dict,
                        url,
                    )
                    logger.info("Ran data_loader")
                    if MODE:
                        partition = event.partition()
                        print(f"Received {data_dict=} from partition {partition}")
                    consumer.commit(event)
                    logger.info("Data insertion committed")
        except KeyboardInterrupt:
            print("Interrupted by user.")
        finally:
            consumer.close()

    producer_node(data_cleaner(raw_data_fetcher(1))) >> consumer_node()


userd_dag()
