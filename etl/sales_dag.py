from datetime import timedelta

from airflow.models import DAG

from airflow.operators.python import PythonOperator


from airflow.utils.dates import days_ago
import json
import pandas as pd

from pathlib import Path


root_ = Path(__file__).parent.parent
entity = '2025-01-05'
source_file = root_ /'source'/f'{entity}.json'
stage_folder = root_ /'stage'
transform_folder = root_ / 'transform'


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
        task_id = 'extract',
        python_callable = extract,
        dag = dag
        )



execute_transform= PythonOperator(
        task_id = 'transform',
        python_callable = transform,
        dag = dag
        )


execute_extract >> execute_transform















            
