from confluent_kafka import Consumer
import json
import os
import sys
from random_data_gen_data_loader import data_loader
import time

MODE = os.getenv("DEV")

USERNAME = "postgres"
PASSWORD = None
IP = None
HOME = os.getenv("HOME")

sys.path.insert(1, HOME + "/bin/de_projects/ETL-using-randomuser-api/")
from config.config import config

with open(
    HOME + "/bin/de_projects/ETL-using-randomuser-api/config/password.txt",
    "r",
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
    HOME + "/bin/de_projects/ETL-using-randomuser-api/config/username.txt",
    "r",
) as username:
    file_input = username.readline()
    if file_input:
        USERNAME = file_input.rstrip("\n")


def set_configs():
    config["group.id"] = 1
    config["auto.offset.reset"] = "earliest"
    config["enable.auto.commit"] = "false"


def assignment_callback(consumer, partitions):
    if MODE:
        for partition in partitions:
            print(f"Assigned to {partition.topic}, partition {partition.partition}")


def procure_data(event) -> dict:
    topic = event.topic()
    value = json.loads(event.value().decode("utf-8"))
    final_dict = {}
    final_dict[topic] = value
    return final_dict


def consume_data():
    set_configs()
    consumer = Consumer(config)
    consumer.subscribe(
        ["main", "login", "location", "identification", "image"],
        on_assign=assignment_callback,
    )

    try:
        time_start = time.time()
        time_til_start = 0
        while time_til_start < 15:
            time_til_start = time.time() - time_start
            event = consumer.poll(1.0)
            if event is None:
                continue
            else:
                data_dict = procure_data(event)
                url = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:5432/test"
                data_loader(
                    data_dict,
                    url,
                )
                partition = event.partition()
                print(f"Received {data_dict=} from partition {partition}")
                consumer.commit(event)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        consumer.close()


if __name__ == "__main__":
    consume_data()
