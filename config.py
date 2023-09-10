import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    class Config:
        env_file = os.getenv("ENV_FILE", "dev.env") 
        env_file_encoding = "utf-8"

    KAFKA_BOOTSTRAP_SERVER: str
    KAFKA_NER_TOPIC: str
    KAFKA_KEYWORDS_TOPIC: str



@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()