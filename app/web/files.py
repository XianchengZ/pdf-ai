import boto3
import os
import tempfile
from typing import Tuple, Dict
from app.web.config import Config

def get_s3_client():
    return boto3.client(
        "s3",
        region_name=Config.AWS_S3_REGION,
        aws_access_key_id=Config.AWS_S3_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_S3_SECRET_ACCESS_KEY
    )


def upload(local_file_path: str, file_id: str) -> Tuple[Dict[str, str], int]:
    client = get_s3_client()

    with open(local_file_path, "rb") as f:
        response = client.put_object(
            Body=f,
            Bucket=Config.AWS_S3_BUCKET_NAME,
            Key=file_id
        )
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        return status_code



def download(file_id):
    return _Download(file_id)


class _Download:
    def __init__(self, file_id):
        self.file_id = file_id
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = ""

    def download(self):
        self.file_path = os.path.join(self.temp_dir.name, self.file_id)
        client = get_s3_client()
        with open(self.file_path, "wb") as file:
            client.download_fileobj(Config.AWS_S3_BUCKET_NAME, self.file_id, file)

        return self.file_path

    def cleanup(self):
        self.temp_dir.cleanup()

    def __enter__(self):
        return self.download()

    def __exit__(self, exc, value, tb):
        self.cleanup()
        return False
