import redis
import pandas as pd
import os
import json

from config import settings


class RedisClient:
    def __init__(self, ):
        self.host = os.environ.get('REDIS_HOST', 'localhost')
        self.port = os.environ.get('REDIS_PORT', 6379)
        self.r = redis.Redis(host=self.host, port=self.port, charset='utf-8', decode_responses=True)
    
    def get_data(self, table) -> dict:
        data = [
            json.loads(element)
            for element in self.r.lrange(table, 0, -1)
        ]
        return pd.DataFrame(data)   

    def delete_data(self, table):
        self.r.delete(table)


if __name__ == '__main__':
    rc = RedisClient()
    df = rc.get_stream_data()
    print(df)