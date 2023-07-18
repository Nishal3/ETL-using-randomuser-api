from sqlalchemy import create_engine
import sys
import os

MODE = os.getenv("DEV")


def data_loader(data, db_url=None):
    table = list(data.keys())[0]
    data_keys = list(list(data.values())[0].keys())
    data_vals = list(list(data.values())[0].values())

    data_vals = ", ".join([f"'{i}'" for i in data_vals])

    if MODE:
        if db_url is None:
            i, j, k = (table, data_keys, data_vals)
            print(i, "\n", j, "\n", k)
            return
    if db_url is None:
        print("Please provide a database url")
        sys.exit(1)

    engine = create_engine(db_url)
    connection = engine.connect()
    print(f"Table: {table}, Columns: {data_keys}, Values: {data_vals}")
    connection.execute(
        f"INSERT INTO {table} ({', '.join(data_keys)}) VALUES ({data_vals})"
    )

    connection.close()
