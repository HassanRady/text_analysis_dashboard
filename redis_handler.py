import redis
import pandas as pd
import os

class RedisClient:
    def __init__(self, ):
        self.host = os.environ.get('REDIS_HOST', 'localhost')
        self.port = os.environ.get('REDIS_PORT', 6379)
        self.r = redis.Redis(host=self.host, port=self.port, charset='utf-8', decode_responses=True)

    def get_stream_data(self,):
        data = {'author_id': [], 'topic': [], 'text': [],}
        keys = self.r.keys()
        for key in keys[:]:
            if "schema" not in key:
                data['author_id'].append(self.r.hget(key, 'author_id'))
                data['topic'].append(self.r.hget(key, 'topic'))
                data['text'].append(self.r.hget(key, 'text'))
        df = pd.DataFrame(data)
        return df


if __name__ == '__main__':
    rc = RedisClient()
    df = rc.get_stream_data()
    print(df)