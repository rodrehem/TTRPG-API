import boto3
import os
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')
S3_ACESS_KEY = os.getenv('S3_ACESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')  

s3_client = boto3.client('s3', region_name= AWS_REGION, aws_access_key_id= S3_ACESS_KEY, aws_secret_access_key=S3_SECRET_KEY)
