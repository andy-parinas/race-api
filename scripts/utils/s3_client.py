import boto3
import os


space_access_key= os.getenv("S3_ACCESS_KEY")
space_secret_key= os.getenv("S3_SECRET")

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='your_spaces_region',
    endpoint_url='https://your_spaces_region.digitaloceanspaces.com',
    aws_access_key_id=space_access_key,
    aws_secret_access_key=space_secret_key
)