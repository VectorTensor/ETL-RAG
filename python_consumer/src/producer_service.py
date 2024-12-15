import os
import time

import boto3
import dotenv
from faker.generator import random
import json

dotenv.load_dotenv()

access_key_id = "AKIAVUPA5TNW2L44QUF5"
access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')

kinesis_client = boto3.client('kinesis',
                              aws_access_key_id=access_key_id,
                              aws_secret_access_key=access_key, region_name=region)

stream_name = 'TextStreamData'

data = {
    'id': random.randint(1, 1000),
    'timestamp': int(time.time()),
    'value': random.uniform(10.0, 100.0)
}

# Convert the data to JSON string
payload = json.dumps(data)
kinesis_client.put_record(StreamName=stream_name, Data=payload, PartitionKey='1')
