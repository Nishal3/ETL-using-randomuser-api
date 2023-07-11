from confluent_kafka import Producer
from kafka_config.config import config
import requests
import json
import time
import os

MODE = os.getenv("DEV")


def extraction(val: dict, key1: str, key2: str = None) -> dict:
    if not key2:
        return val[key1]
    else:
        return val[key1][key2] if isinstance(val[key1][key2], dict) else {}


def callback(err, event):
    if err:
        print(
            f"Produce to topic {event.topic()} failed for event: {event.key()}, {err}"
        )
    else:
        val = event.value().decode("utf8")
        if MODE:
            print(f"{val}, sent to partition {event.partition()}.")


def export_data(producer, key, value):
    producer.produce("hello_topic", value, key, on_delivery=callback)


def production_loop(random_person_data, results):
    final_results = {}

    for i in results:
        if not isinstance(random_person_data["results"][0][i], dict):
            final_results[i] = random_person_data["results"][0][i]

    return final_results


def produce_data(time_seconds=0.1):
    # Producer Stuff
    producer = Producer(config)

    # API Stuff
    api_link = "https://randomuser.me/api/"
    # print(thing.text)
    time_start = time.time()
    time_from_start = 0

    while time_from_start < time_seconds:
        api = requests.get(api_link)
        random_person_data = json.loads(api.text)
        results = random_person_data["results"][0]
        key = extraction(results, "login")["uuid"]

        final_results = production_loop(random_person_data, results)

        final_results = json.dumps(final_results, indent=4)
        export_data(producer, key, final_results)

        time_from_start = time.time() - time_start
    producer.flush()


if __name__ == "__main__":
    produce_data(1)
