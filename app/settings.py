import os
import pathlib
from pydantic import BaseSettings, PostgresDsn, Field
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_VI: str = "/api/v1"
    JWT_SECRET: str = "DO_NOT_USE_IN_PRODUCTION"

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")



settings = Settings()

print(f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?sslmode=require")