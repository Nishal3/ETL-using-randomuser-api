from confluent_kafka import Producer
import json
import os
import sys
import time

sys.path.insert(1, "/home/ubuntu/ETL-using-randomuser-api/")

from kafka_config.config import config

MODE = os.getenv("DEV")


def callback(err, event):
    if err:
        print(
            f"Produce to topic {event.topic()} failed for event: {event.key()}, {err}."
        )
    else:
        if MODE:
            val = event.value().decode("utf8")
            print(
                f"Topic: {event.topic()}\n Value: {val}, sent to partition {event.partition()}."
            )


def export_data(producer, key, value, topic):
    producer.produce(topic, value, key, on_delivery=callback)


def production_loop(producer, results):
    uuid = results["main"]["uuid"]
    for i, j in results.items():
        j = json.dumps(j, indent=4)
        export_data(producer, uuid, j, i)


def produce_data():
    producer = Producer(config)

    with open("cleaned_user_data.json", "r") as data:
        results = json.load(data)

    for i in results:
        production_loop(producer, i)
        producer.flush()

    print(results)


if __name__ == "__main__":
    produce_data()
