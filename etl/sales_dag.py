from datetime import timedelta

from airflow.models import DAG

from airflow.operators.python import PythonOperator


from airflow.utils.dates import days_ago
import json
import pandas as pd
import os
from dotenv import load_dotenv

from pathlib import Path
from sqlalchemy import create_engine

load_dotenv(dotenv_path='/home/prayash/Prayash/ETL-RAG/etl/.env')
host = os.getenv('host')

user = os.getenv('user')
password = os.getenv('password')
dbname = os.getenv('dbname')

root_ = Path(__file__).parent.parent
entity = '2025-01-05'
source_file = root_ / 'source'/f'{entity}.json'
stage_folder = root_ / 'stage'
transform_folder = root_ / 'transform'


connection_string = f"postgresql+psycopg2://{user}:{password}@" \
    f"{host}:{5432}/{dbname}"


def extract():

    df_stage = {
        "product_id": [],
        "customer_id": [],
        "cogs": [],
        "quantity": [],
        "unit_sale_price": []
    }
    df_stage = pd.DataFrame(df_stage)
    with open(source_file, 'r') as infile:

        data_json = json.load(infile)

        for data in data_json:

            df_stage.loc[len(df_stage)] = data.values()

    df_stage.to_csv(str(stage_folder)+"/"+entity+'.csv')


def transform():

    df = pd.read_csv(str(stage_folder)+"/"+entity+'.csv')

    df['total_price'] = df['unit_sale_price'] * df['quantity']

    df.to_csv(str(transform_folder)+"/"+entity+'.csv')


def load(connection_string_):
    print("prayash"+connection_string_)

    engine = create_engine(connection_string_)

    df = pd.read_csv(str(transform_folder)+'/'+entity+'.csv')

    df.to_sql("sales", engine, if_exists='append', index=False)

    print("Data loaded successfully into PostgreSQL.")


default_args = {
    'owner': 'Prayash Thapa',
    'start_date': days_ago(0),
    'email': ['prayashthapa15@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# Define the DAG
dag = DAG(
    'sales-dag',
    default_args=default_args,
    description='dag to extract sales data from s3',
    schedule_interval=timedelta(days=1),
)

execute_extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag
)


execute_transform = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag
)

execute_load = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag,
    op_kwargs={
        'connection_string_': connection_string
    }
)


execute_extract >> execute_transform >> execute_load
