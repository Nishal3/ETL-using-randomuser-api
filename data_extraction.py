import requests
import json
import pandas as pd
import time


def extraction(val: dict, key1: str, key2: str = None) -> dict:
    if not key2:
        return val[key1]
    else:
        return val[key1][key2] if isinstance(val[key1][key2], dict) else {}


api_link = "https://randomuser.me/api/"
# print(thing.text)

for i in range(20):
    thing = requests.get(api_link)
    random_person_data = json.loads(thing.text)
    results = random_person_data["results"][0]

    # print(type(json.loads(thing.text)))

    name = extraction(results, "name")
    location = extraction(results, "location")
    location_street = extraction(location, "street")
    location_timezone = extraction(location, "timezone")
    location_coordinates = extraction(location, "coordinates")
    login = extraction(results, "login")
    dob = extraction(results, "dob")
    registered = extraction(results, "registered")
    id = extraction(results, "id")
    picture = extraction(results, "picture")
    fin_results = {}

    for i in random_person_data["results"][0]:
        if not isinstance(random_person_data["results"][0][i], dict):
            results[i] = random_person_data["results"][0][i]

    collected_data = [name, location, login, dob, registered, id, picture, fin_results]
    # for i in collected_data:
    #     print(i, "\n" + "-" * 50, "\n")

    print(location_street, location_coordinates, location_timezone)
