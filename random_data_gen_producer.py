from confluent_kafka import Producer
from kafka_config.config import config
import requests
import json
import time
import random
import os
import sys

MODE = os.getenv("DEV")


def extraction(val: dict, key1: str, key2: str = None) -> dict:
    if not key2:
        return val[key1]
    else:
        return val[key1][key2] if val[key1][key2] else {}


def callback(err, event):
    if err:
        print(
            f"Produce to topic {event.topic()} failed for event: {event.key()}, {err}"
        )
    else:
        val = event.value().decode("utf8")
        if MODE:
            print(
                f"Topic: {event.topic()}\n Value: {val}, sent to partition {event.partition()}."
            )


def export_data(producer, key, value, topic):
    producer.produce(topic, value, key, on_delivery=callback)


def production_loop(producer, final_results):
    uuid = final_results["main"]["uuid"]
    for i, j in final_results.items():
        j = json.dumps(j, indent=4)
        export_data(producer, uuid, j, i)


def main_table(results):
    uuid = extraction(results, "login")["uuid"]
    location_coordinates = (
        extraction(results, "location", "coordinates")["latitude"],
        extraction(results, "location", "coordinates")["longitude"],
    )
    email = results["email"]
    thumbnail = extraction(results, "picture")["thumbnail"]

    temp_addition = [uuid, location_coordinates, email, thumbnail]
    temp_list = ["uuid", "location_coordinates", "email", "thumbnail"]

    main = {}

    for i, j in zip(temp_list, temp_addition):
        main[i] = j

    return main


def login_table(results):
    login = {}

    uuid = extraction(results, "login")["uuid"]
    username = extraction(results, "login")["username"]
    password = extraction(results, "login")["password"]
    temp_addition = [uuid, username, password]
    temp_list = ["uuid", "username", "password"]
    for i, j in zip(temp_list, temp_addition):
        login[i] = j

    return login


def location_table(results):
    location = {}

    location_coordinates = (
        extraction(results, "location", "coordinates")["latitude"],
        extraction(results, "location", "coordinates")["longitude"],
    )
    street_name = extraction(results, "location", "street")["name"]
    street_number = extraction(results, "location", "street")["number"]
    city = extraction(results, "location")["city"]
    state = extraction(results, "location")["state"]
    country = extraction(results, "location")["country"]
    post_code = extraction(results, "location")["postcode"]
    timezone = extraction(results, "location", "timezone")["offset"]

    temp_addition = [
        location_coordinates,
        street_name,
        street_number,
        city,
        state,
        country,
        post_code,
        timezone,
    ]
    temp_list = [
        "location_coordinates",
        "street_name",
        "street_number",
        "city",
        "state",
        "country",
        "post_code",
        "timezone",
    ]

    for i, j in zip(temp_list, temp_addition):
        location[i] = j

    return location


def identification_table(results):
    identification = {}

    email = results["email"]
    id = (extraction(results, "id")["value"], extraction(results, "id")["name"])
    name = extraction(results, "name", "first")
    last_name = extraction(results, "name", "last")
    gender = results["gender"]
    phone = results["phone"]
    cell = results["cell"]
    nationality = results["nat"]
    dob = extraction(results, "dob", "date")
    registered = extraction(results, "registered", "date")

    temp_addition = [
        email,
        id,
        name,
        last_name,
        gender,
        phone,
        cell,
        nationality,
        dob,
        registered,
    ]
    temp_list = [
        "email",
        "id",
        "name",
        "last_name",
        "gender",
        "phone",
        "cell",
        "nationality",
        "dob",
        "registered",
    ]

    for i, j in zip(temp_list, temp_addition):
        identification[i] = j

    return identification


def image_table(results):
    image = {}

    thumbnail = extraction(results, "picture")["thumbnail"]
    large = extraction(results, "picture", "large")
    medium = extraction(results, "picture", "medium")

    temp_addition = [thumbnail, large, medium]
    temp_list = ["thumbnail", "large", "medium"]

    for i, j in zip(temp_list, temp_addition):
        image[i] = j

    return image


def assemble_data(results) -> dict:
    final = {}

    final["main"] = main_table(results)
    final["login"] = login_table(results)
    final["location"] = location_table(results)
    final["identification"] = identification_table(results)
    final["image"] = image_table(results)

    return final


def produce_data(api_link):
    # Producer Stuff
    producer = Producer(config)

    # API Stuff
    api_link = "https://randomuser.me/api/"
    # # print(thing.text)
    # time_start = time.time()
    # time_from_start = 0

    # while time_from_start < 3600:
    try:
        api = requests.get(api_link)
        random_person_data = json.loads(api.text)
        results = random_person_data["results"][0]

        final_results = assemble_data(results)

        production_loop(producer, final_results)

        # time_from_start = time.time() - time_start
        producer.flush()
    except:
        sys.exit(1)


def production_scheduler():
    data_throughput = random.randint(1, 3600)
    time_to_next_fetch = 3590 / data_throughput
    time_start = time.time()
    time_til_start = 0
    api_link = "https://randomuser.me/api/"
    while time_til_start < 3600:
        time.sleep(time_to_next_fetch)
        produce_data(api_link)
        time_til_start = time.time() - time_start


# if __name__ == "__main__":
#     produce_data()
