import redis
import pandas as pd
import os

from config import settings

class RedisClient:
    def __init__(self, ):
        self.host = os.environ.get('REDIS_HOST', 'localhost')
        self.port = os.environ.get('REDIS_PORT', 6379)
        self.r = redis.Redis(host=self.host, port=self.port, charset='utf-8', decode_responses=True)
    
    def get_stream_data(self, table):
        keys = self.r.scan_iter(match=f'{table}:*')
        data = {'text': [],}
        for key in keys:
            # data['author_id'].append(self.r.hget(key, 'author_id'))
            data['text'].append(self.r.hget(key, 'output'))
        return pd.DataFrame(data)
    
    def delete_stream_data(self, table):
        keys = self.r.scan_iter(match=f'{table}:*')
        for key in keys:
            self.r.delete(key)

    def set_key(self, key, value):
        self.r.set(key, value)

    def get_key(self, key):
        return self.r.get(key)

    def delete_key(self, key):
        self.r.delete(key)

    def write_to_table(self, table, timestamp, data):
        data = {k: " ".join(v) for k, v in data.items()}
        self.r.hmset(f"{table}:{timestamp}", data)


if __name__ == '__main__':
    rc = RedisClient()
    df = rc.get_stream_data()
    print(df)