import pathlib
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VI: str = "/api/v1"
    JWT_SECRET: str = "DO_NOT_USE_IN_PRODUCTION"
    SQLALCHEMY_DATABASE_URI: str = "postgresql://db_user:password123@localhost:5432/race_analyst"

    class Config:
        case_sensitive = True


settings = Settings()