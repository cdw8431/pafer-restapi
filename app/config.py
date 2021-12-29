import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv(verbose=True)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URL: Optional[PostgresDsn] = PostgresDsn.build(
        scheme="postgresql",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=f"{os.getenv('POSTGRES_SERVER')}:{os.getenv('POSTGRES_PORT')}",
        path=f"/{os.getenv('POSTGRES_DB')}",
    )


settings = Settings()
