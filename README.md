# Information
Python version 3.10 and Airflow version 2.6.3 used.
## Description
![ETL]
Simple ETL using Apache Airflow, Kafka and AWS using the [randomuser API][API]. Messages are delivered every 5 minutes and data output is randomized from 1 to 150 inputs. 

## Tools Used:  
  * Apache Kafka
  * Apache Airflow 
  * AWS EC2
  * AWS RDS
  * PostgreSQL Database

## Setup
As mentioned before make sure you are using Python 3.10, >=3.6 might also work, but not advised. First install all of the dependencies.

Airflow:  
Taken from the [airflow quickstart guide][AIRFLOW_QS].
``` bash
# Exporting home is optional unless you want it to be in a specific place
export AIRFLOW_HOME=~/airflow
# Set version of Airflow
AIRFLOW_VERSION=2.7.2
# Get Python version, should be 3.10
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# Constraint URL for installation
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# Installation
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

confluent_kafka:
``` bash
pip install confluent-kafka
```

sqlalchemy:
``` bash
pip install sqlalchemy
pip install psycopg2-binary
```



[API]: http://randomuser.me/api
[ETL]: https://raw.githubusercontent.com/Nishal3/ETL-using-randomuser-api/assets/User_Data_ETL.jpeg
[AIRFLOW_QS]: https://airflow.apache.org/docs/apache-airflow/stable/start.html

