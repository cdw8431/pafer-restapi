import json
from typing import Optional

from pydantic import BaseSettings, PostgresDsn

with open("settings.json") as f:
    config = json.loads(f.read())


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URL: Optional[PostgresDsn] = PostgresDsn.build(
        scheme="postgresql",
        user=config.get("POSTGRES_USER"),
        password=config.get("POSTGRES_PASSWORD"),
        host=f"{config.get('POSTGRES_SERVER')}:{config.get('POSTGRES_PORT')}",
        path=f"/{config.get('POSTGRES_DB')}",
    )


settings = Settings()
