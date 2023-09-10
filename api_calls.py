import requests
import os

import logger

_logger = logger.get_logger(__name__)

CASSANDRA_READER_HOST = os.environ.get('CASSANDRA_READER_HOST', 'localhost')
CASSANDRA_READER_PORT = os.environ.get('CASSANDRA_READER_PORT', '9042')
CASSANDRA_READER_URL = f"http://{CASSANDRA_READER_HOST}:{CASSANDRA_READER_PORT}"

TWITTER_HANDLER_API_HOST = os.environ.get('TWITTER_HANDLER_API_HOST', 'localhost')
TWITTER_HANDLER_API_PORT = os.environ.get('TWITTER_HANDLER_API_PORT', 9001)
TWITTER_HANDLER_API_URL = f"http://{TWITTER_HANDLER_API_HOST}:{TWITTER_HANDLER_API_PORT}"

SPARK_STREAM_API_HOST = os.environ.get('SPARK_STREAM_API_HOST', 'localhost')
SPARK_STREAM_API_PORT = os.environ.get('SPARK_STREAM_API_PORT', 9000)
SPARK_STREAM_API_URL = f"http://{SPARK_STREAM_API_HOST}:{SPARK_STREAM_API_PORT}"

TRENDING_HASHTAGS_SERVICE_HOST = os.environ.get('TRENDING_HASHTAGS_SERVICE_HOST', 'localhost')
TRENDING_HASHTAGS_SERVICE_PORT = os.environ.get('TRENDING_HASHTAGS_SERVICE_PORT', 9011)
TRENDING_HASHTAGS_SERVICE_URL = f"http://{TRENDING_HASHTAGS_SERVICE_HOST}:{TRENDING_HASHTAGS_SERVICE_PORT}"

SENTIMENT_MODEL_SERVICE_HOST = os.environ.get('SENTIMENT_MODEL_SERVICE_HOST', 'localhost')
SENTIMENT_MODEL_SERVICE_PORT = os.environ.get('SENTIMENT_MODEL_SERVICE_PORT', 9011)
SENTIMENT_MODEL_SERVICE_URL = f"http://{SENTIMENT_MODEL_SERVICE_HOST}:{SENTIMENT_MODEL_SERVICE_PORT}"

EMOTION_MODEL_SERVICE_HOST = os.environ.get('EMOTION_MODEL_SERVICE_HOST', 'localhost')
EMOTION_MODEL_SERVICE_PORT = os.environ.get('EMOTION_MODEL_SERVICE_PORT', 9012)
EMOTION_MODEL_SERVICE_URL = f"http://{EMOTION_MODEL_SERVICE_HOST}:{EMOTION_MODEL_SERVICE_PORT}"

KEYWORD_EXTRACTION_SERVICE_HOST = os.environ.get('KEYWORD_EXTRACTION_SERVICE_HOST', 'localhost')
KEYWORD_EXTRACTION_SERVICE_PORT = os.environ.get('KEYWORD_EXTRACTION_SERVICE_PORT', 9013)
KEYWORD_EXTRACTION_SERVICE_URL = f"http://{KEYWORD_EXTRACTION_SERVICE_HOST}:{KEYWORD_EXTRACTION_SERVICE_PORT}"

NAMED_ENTITY_RECOGNITION_SERVICE_HOST = os.environ.get('NAMED_ENTITY_RECOGNITION_SERVICE_HOST', 'localhost')
NAMED_ENTITY_RECOGNITION_SERVICE_PORT = os.environ.get('NAMED_ENTITY_RECOGNITION_SERVICE_PORT', 9014)
NAMED_ENTITY_RECOGNITION_SERVICE_URL = f"http://{NAMED_ENTITY_RECOGNITION_SERVICE_HOST}:{NAMED_ENTITY_RECOGNITION_SERVICE_PORT}"


class API:
    def __init__(self):
        pass

    def start_stream(self, topic):
        def _start_stream(topic):
            s = requests.get(
                f"{TWITTER_HANDLER_API_URL}/start", params={"topic": topic})
            s2 = requests.get(
            f"{SPARK_STREAM_API_URL}/start")
        _start_stream(topic)

    def stop_stream(self):
        response = requests.get(f"{TWITTER_HANDLER_API_URL}/stop")
        response = requests.get(f"{SPARK_STREAM_API_URL}/stop")
        return response.text

    def get_offline_data(self):
        import pandas as pd
        df = pd.read_csv("data.csv")
        return df.to_json(orient='records')        

    def get_trending(self, WOEID=1):
        response = requests.get(f"{TRENDING_HASHTAGS_SERVICE_URL}/trending_hashtags", params={f'WOEID': WOEID})
        return response.json()

    def get_ner(self, text):
        url = f"{NAMED_ENTITY_RECOGNITION_SERVICE_URL}/ner"
        field = 'text'
        body  = {field: text.tolist()}
        response = requests.post(url=url, json=body)
        return response.json()

    def extract_keywords(self, text):
        url = f"{KEYWORD_EXTRACTION_SERVICE_URL}/extract"
        field = 'text'
        body  = {field: text.tolist()}
        response = requests.post(url=url, json=body)
        return response.json()

    def predict_emotion(self, df):
        X = df['text']
        body = {'inputs': X.tolist()}
        request = requests.post(f'{EMOTION_MODEL_SERVICE_URL}/v1/models/emotion/versions/1:predict', json=body)
        request_json = request.json()
        request_json['text'] = X
        request_json['author_id'] = df['author_id']
        return request_json

    def predict_sentiment(self, df):
        X = df['text']
        body = {'inputs': X.tolist()}
        request = requests.post(f'{SENTIMENT_MODEL_SERVICE_URL}/v1/models/sentiment/labels/production:predict', json=body)
        request_json = request.json()
        request_json['text'] = X
        request_json['author_id'] = df['author_id']
        return request_json