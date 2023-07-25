from sqlalchemy import create_engine
from sqlalchemy import text
import sys
import os

MODE = os.getenv("DEV")


def data_loader(data, db_url=None):
    table = list(data.keys())[0]
    data_keys = list(list(data.values())[0].keys())
    data_vals = list(list(data.values())[0].values())

    data_vals = ", ".join(
        [
            f"'{i}'" if isinstance(i, int) or isinstance(i, str) else f"ARRAY{i}"
            for i in data_vals
        ]
    )

    if MODE:
        print(f"Table: {table}, Columns: {data_keys}, Values: {data_vals}")
    if db_url is None:
        print("Please provide a database url")
        sys.exit(1)

    engine = create_engine(db_url)
    connection = engine.connect()
    print(f"Table: {table}, Columns: {data_keys}, Values: {data_vals}")
    connection.execute(
        text(f"INSERT INTO {table} ({', '.join(data_keys)}) VALUES ({data_vals})")
    )

    connection.commit()
    connection.close()

if __name__ == "__main__":
    engine = create_engine("postgresql://postgres:k7UlpPL%251E#e@192.168.0.249:5432/test")
    conn = engine.connect()
    
