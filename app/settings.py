import pathlib
from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    API_VI: str = "/api/v1"
    JWT_SECRET: str = "DO_NOT_USE_IN_PRODUCTION"
    # DB_HOST: str = "localhost"
    # DB_PORT: int = 5432
    # DB_NAME: str = "race_analyst"
    # DB_USER: str = "db_user"
    # DB_PASSWORD: str = "password123"


    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field("race_analyst", env="DB_NAME")
    DB_USER: str = Field("db_user", env="DB_USER")
    DB_PASSWORD: str = Field("password123", env="DB_PASSWORD")
    # SQLALCHEMY_DATABASE_URI: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    class Config:
        case_sensitive = True


settings = Settings()

print(f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")