import json
import sys
from confluent_kafka import Consumer
import os

sys.path.insert(1, "/home/nish/bin/de_projects/ETL-using-randomuser-api")
from kafka_config.config import config as main_config

MODE = os.getenv("DEV")


def set_configs():
    config = main_config
    config["group.id"] = 1
    config["auto.offset.reset"] = "earliest"
    config["enable.auto.commit"] = "false"
    return config


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
