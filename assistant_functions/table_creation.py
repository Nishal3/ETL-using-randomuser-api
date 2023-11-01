from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
import os

USERNAME = ""
PASSWORD = ""
IP = ""
HOME = os.getenv("HOME")

with open(
    HOME + "/bin/de_projects/ETL-using-randomuser-api/config/password.txt", "r"
) as password:
    file_input = password.readline()
    if file_input:
        PASSWORD = file_input.rstrip("\n")

with open(
    HOME + "/bin/de_projects/ETL-using-randomuser-api/config/ip_address.txt", "r"
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

URL = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:5432/"

try:
    engine = create_engine(URL, future=True)
    conn = engine.connect()
    print("CONNECTED")
    conn.execute(text("commit"))
    conn.execute(text("create database user_data"))
    conn.execute(text("commit"))
    print("SUCCESSFULLY CREATED DATABASE")

except ProgrammingError as e:
    print(f"error: {e}")

finally:
    conn.close()
URL += "user_data"

engine = create_engine(URL, future=True)
conn = engine.connect()
conn.execute(text("commit"))
query = "\
    /* main */\
	create table main (\
		recordid serial,\
		uuid varchar,\
		location_coordinates text[],\
		email varchar,\
		thumbnail varchar\
	);\
\
	/* login */\
	create table login (\
		uuid varchar,\
		username varchar,\
		password varchar\
	);\
\
	/* location */\
	create table location (\
		location_coordinates text[],\
		street_name varchar,\
		street_number int,\
		city varchar,\
		state varchar,\
		country varchar,\
		post_code varchar,\
		timezone varchar\
	);\
\
	/* identification */\
	create table identification (\
		email varchar,\
		id text[],\
		name varchar,\
		last_name varchar,\
		gender varchar,\
		phone varchar,\
		cell varchar,\
		nationality varchar,\
		dob timestamp,\
		registered timestamp\
	);\
\
	/* image */\
	create table image (\
		thumbnail varchar,\
		large varchar,\
		medium varchar\
	);"
try:
    conn.execute(text(query))
    conn.commit()
    print("SUCCESSFULLY CREATED TABLES")
except ProgrammingError as e:
    print(f"error: {e}")
finally:
    conn.close()
