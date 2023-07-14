from confluent_kafka import Consumer
from kafka_config.config import config
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

MODE = os.getenv("DEV")


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


def load_data(data=dict, host=None, username=None, password=None, database=None):
    if host is None and username is None and password is None:
        i, j = (list(data.keys())[0], list(data.values())[0])
        print(i, "\n", j)
        return
    if None in [host, username, password]:
        if host is None:
            print("Please provide a host")
        if username is None:
            print("Please provide a username")
        if password is None:
            print("Please provide a password")
        sys.exit(1)


if __name__ == "__main__":
    set_configs()
    consumer = Consumer(config)
    consumer.subscribe(
        ["main", "login", "location", "identification", "image"],
        on_assign=assignment_callback,
    )

    try:
        while True:
            event = consumer.poll(1.0)
            if event is None:
                continue
            else:
                data_dict = procure_data(event)
                load_data(data_dict, "localhost")
                partition = event.partition()
                print(f"Received {data_dict=} from partition {partition}")
                consumer.commit(event)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        consumer.close()
