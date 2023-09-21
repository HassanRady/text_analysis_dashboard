import redis
import pandas as pd
import json

from config import settings


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, charset='utf-8', decode_responses=True)

class RedisClient:
    @staticmethod
    def get_data_from_list(key: str) -> pd.DataFrame:
        data = [
            json.loads(element)
            for element in r.lrange(key, 0, -1)
        ]
        return data


    @staticmethod
    def delete_key(key: str):
        r.delete(key)


if __name__ == '__main__':
    rc = RedisClient()
    df = rc.get_data_from_list(settings.KAFKA_KEYWORDS_TOPIC)
    print(df)