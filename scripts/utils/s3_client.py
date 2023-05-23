import boto3
import os
from app.settings import settings


class S3Client:

    def __init__(self) -> None:
        session = boto3.session.Session()
        self.client = session.client(
            's3',
            region_name='syd1',
            endpoint_url='https://mi4orm-form-data.syd1.digitaloceanspaces.com',
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


s3_client = S3Client()
