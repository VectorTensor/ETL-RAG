import os
import time

import boto3
import dotenv

from src.model_communicator_service import FoundationModel
from src.producer_service import stream_data

dotenv.load_dotenv()

access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')

firehose_client = boto3.client('firehose', aws_access_key_id=access_key_id,
                               aws_secret_access_key=access_key, region_name=region)

# Define the delivery stream name
delivery_stream_name = "dataeng-firehose-streaming-s3"

if __name__ == '__main__':
    client_bedrock = boto3.client('bedrock-runtime',
                                  aws_access_key_id=access_key_id,
                                  aws_secret_access_key=access_key, region_name=region)  # Use your region

    foundation_model = FoundationModel(client_bedrock)

    stream_data(firehose_client, 'dataeng-firehose-streaming-s3', foundation_model)
