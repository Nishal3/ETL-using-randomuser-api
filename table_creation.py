from sqlalchemy import create_engine
from sqlalchemy import text

USERNAME = "postgres"
PASSWORD = None
IP = None

with open(
    "/home/ubuntu/ETL-using-randomuser-api/kafka_config/password.txt", "r"
) as password:
    file_input = password.readline()
    if file_input:
        PASSWORD = file_input.rstrip("\n")

with open(
    "/home/ubuntu/ETL-using-randomuser-api/kafka_config/ip_address.txt", "r"
) as ip_address:
    file_input = ip_address.readline()
    if file_input:
        IP = file_input.rstrip("\n")

with open(
    "/home/ubuntu/ETL-using-randomuser-api/kafka_config/username.txt", "r"
) as username:
    file_input = username.readline()
    if file_input:
        USERNAME = file_input.rstrip("\n")

print(f"postgresql://{USERNAME}:{PASSWORD}@{IP}:5432/")

URL = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:5432/"

engine = create_engine(URL, future=True)
conn = engine.connect()
conn.execute(text("commit"))
print("CONNECTED")
conn.execute(text("CREATE DATABASE user_data;"))
conn.commit()

conn.close()


