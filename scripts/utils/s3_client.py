import boto3
import os
from app.settings import settings


class S3Client:

    def __init__(self, region, endpoint) -> None:
        session = boto3.session.Session()
        self.client = session.client(
            's3',
            region_name=region,
            endpoint_url=endpoint,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET
        )

    def upload_file(self, file_name: str, bucket: str, object_name: str = None) -> bool:
        if object_name is None:
            object_name = file_name

        try:
            response = self.client.upload_file(file_name, bucket, object_name)
            return True
        except Exception as e:
            print(e)
            return False

    def upload_image(self, object_data, bucket, object_name):
        content_type = 'image/jpeg'
        try:
            response = self.client.put_object(
                Body=object_data, Bucket=bucket, Key=object_name, ContentType=content_type)

            return True
        except Exception as e:
            print(e)
            return False

    def make_object_public(self, bucket, object_name):
        self.client.put_object_acl(
            ACL='public-read',
            Bucket=bucket,
            Key=object_name
        )

# s3_client = S3Client()
