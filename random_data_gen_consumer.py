from confluent_kafka import Consumer
from kafka_config.config import config
import os

MODE = os.getenv("DEV")


def set_configs():
    config["group.id"] = 1
    config["auto.offset.reset"] = "earliest"
    config["enable.auto.commit"] = "false"


def assignment_callback(consumer, partitions):
    if MODE:
        for partition in partitions:
            print(f"Assigned to {partition.topic}, partition {partition.partition}")


if __name__ == "__main__":
    set_configs()
    consumer = Consumer(config)
    consumer.subscribe(["hello_topic"], on_assign=assignment_callback)
    try:
        while True:
            event = consumer.poll(1.0)
            if event is None:
                continue
            else:
                val = event.value().decode("utf-8")
                partition = event.partition()
                print(f"Received {val} from partition {partition}")
                consumer.commit(event)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        consumer.close()
