import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SESSION_PERMANENT = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    CELERY = {
        "broker_url": os.environ.get("REDIS_URI", False),
        "task_ignore_result": True,
        "broker_connection_retry_on_startup": False,
    }
    AWS_S3_REGION = os.environ["AWS_S3_REGION"]
    AWS_S3_ACCESS_KEY = os.environ["AWS_S3_ACCESS_KEY"]
    AWS_S3_SECRET_ACCESS_KEY = os.environ["AWS_S3_SECRET_ACCESS_KEY"]
    AWS_S3_BUCKET_NAME = os.environ["AWS_S3_BUCKET_NAME"]
