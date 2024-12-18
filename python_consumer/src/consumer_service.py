import os
import time
import boto3
import dotenv
from faker.generator import random
import json

dotenv.load_dotenv()

access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')

kinesis_client = boto3.client('kinesis',
                              aws_access_key_id=access_key_id,
                              aws_secret_access_key=access_key, region_name=region)

stream_name = 'TextStreamData'
response = kinesis_client.describe_stream(StreamName=stream_name)
shard_id = response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator_response = kinesis_client.get_shard_iterator(
    StreamName=stream_name,
    ShardId=shard_id,
    ShardIteratorType='TRIM_HORIZON'  # Reads from the beginning of the stream
)

shard_iterator = shard_iterator_response['ShardIterator']

# Poll for records
while True:
    response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=10)
    shard_iterator = response['NextShardIterator']

    # Print records
    for record in response['Records']:
        print(f"Record: {record['Data'].decode('utf-8')}")

    # Wait before fetching the next set of records
    time.sleep(1)