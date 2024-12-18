import os
import boto3
import dotenv

dotenv.load_dotenv()

access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')

