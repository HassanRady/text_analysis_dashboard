import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    class Config:
        env_file = os.getenv("ENV_FILE", "dev.env") 
        env_file_encoding = "utf-8"

    REDIS_HOST: str
    REDIS_PORT: int

    KAFKA_NER_TOPIC: str
    KAFKA_KEYWORDS_TOPIC: str
    KAFKA_SENTIMENT_TOPIC: str
    KAFKA_EMOTION_TOPIC: str

    WORDCLOUD_SERVICE_URL: str
    TREND_SUBREDDIT_SERVICE_URL: str



@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()