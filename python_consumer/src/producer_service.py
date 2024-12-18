import os
import time

import boto3
import dotenv

from src.model_communicator_service import FoundationModel

dotenv.load_dotenv()

access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')


def stream_data(client, stream_, foundation_model_: FoundationModel):
    message = foundation_model_.get_fake_letter()
    while True:
        response = client.put_record(
            DeliveryStreamName=stream_,
            Record={"Data": f'{{"message":"{message}"}}'}
        )
        print("PutRecord Response:", response)
        time.sleep(10)
