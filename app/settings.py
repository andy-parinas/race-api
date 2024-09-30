import os
import pathlib
from pydantic import BaseSettings, PostgresDsn, Field
from dotenv import load_dotenv

load_dotenv()


settings_directory = os.path.dirname(os.path.abspath(__file__))
storage_directory = os.path.abspath(
    os.path.join(settings_directory, '..', 'storage'))


class Settings:

    API_VI: str = "/api/v1"
    JWT_SECRET: str = "DO_NOT_USE_IN_PRODUCTION"

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    SSL_MODE = os.getenv("SSL_MODE", "disable")

    # SFTP Configuration

    SFTP_HOST = os.getenv("SFTP_HOST")
    SFTP_PORT = os.getenv("SFTP_PORT", 22)
    SFTP_PRIVATE_KEY = os.getenv(
        "SFTP_PRIVATE_KEY", f"{storage_directory}/sftp_key")
    SFTP_USERNAME = os.getenv("SFTP_USERNAME")

    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET = os.getenv("S3_SECRET")
    S3_REGION = os.getenv("S3_REGION")

    FORM_BUCKET = os.getenv("FORM_BUCKET")
    IMAGE_BUCKET = os.getenv("IMAGE_BUCKET")

    IMAGE_FOLDER = os.getenv("IMAGE_FOLDER")
    FORM_FOLDER = os.getenv("FORM_FOLDER")
    SCRATCH_FOLDER = os.getenv("SCRATCH_FOLDER")

    IMAGE_URL = os.getenv("IMAGE_URL")


settings = Settings()

# print(f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?sslmode={settings.SSL_MODE}")
