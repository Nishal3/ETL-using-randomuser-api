import requests
import json
import pandas as pd


def extraction(val: dict, key1: str, key2: str = None) -> dict:
    if not key2:
        return val[key1]
    else:
        return val[key1][key2] if val[key1][key2] else {}


api_link = "https://randomuser.me/api/"
# print(thing.text)

thing = requests.get(api_link)
random_person_data = json.loads(thing.text)
results = random_person_data["results"][0]

# print(type(json.loads(thing.text)))

# Stuff

name = extraction(results, "name")
location = extraction(results, "location")
location_street = extraction(location, "street")
location_timezone = extraction(location, "timezone")
location_coordinates = (
    extraction(location, "coordinates")["latitude"],
    extraction(location, "coordinates")["longitude"],
)

login = extraction(results, "login")
dob = extraction(results, "dob")
registered = extraction(results, "registered")
id = extraction(results, "id")
picture = extraction(results, "picture")
fin_results = {}

for i in random_person_data["results"][0]:
    if not isinstance(random_person_data["results"][0][i], dict):
        fin_results[i] = random_person_data["results"][0][i]

collected_data = [name, location, login, dob, registered, id, picture, fin_results]
# for i in collected_data:
#     print(i, "\n" + "-" * 50, "\n")

# For main table
uuid = extraction(results, "login")["uuid"]
location_coordinates = (
    extraction(location, "coordinates")["latitude"],
    extraction(location, "coordinates")["longitude"],
)
email = results["email"]
thumbnail = extraction(results, "picture")["thumbnail"]

temp_addition = [uuid, location_coordinates, email, thumbnail]
temp_list = ["uuid", "location_coordinates", "email", "thumbnail"]

main = {}

for i, j in zip(temp_list, temp_addition):
    main[i] = j
print(main, end="\n\n")

# Login Info
login = {}

username = extraction(results, "login")["username"]
password = extraction(results, "login")["password"]
temp_addition = [uuid, username, password]
temp_list = ["uuid", "username", "password"]
for i, j in zip(temp_list, temp_addition):
    login[i] = j

print(login, end="\n\n")

# Location
location = {}
street_name = location_street["name"]
street_number = location_street["number"]
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

print(location, end="\n\n")

# Identification
identification = {}

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

print(identification, end="\n\n")

# Image
image = {}
large = extraction(results, "picture", "large")
medium = extraction(results, "picture", "medium")

temp_addition = [thumbnail, large, medium]
temp_list = ["thumbnail", "large", "medium"]

for i, j in zip(temp_list, temp_addition):
    image[i] = j

print(image)
