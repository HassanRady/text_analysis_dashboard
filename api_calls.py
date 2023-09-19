import requests
import os



SENTIMENT_MODEL_SERVICE_HOST = os.environ.get('SENTIMENT_MODEL_SERVICE_HOST', 'localhost')
SENTIMENT_MODEL_SERVICE_PORT = os.environ.get('SENTIMENT_MODEL_SERVICE_PORT', 8051)
SENTIMENT_MODEL_SERVICE_URL = f"http://{SENTIMENT_MODEL_SERVICE_HOST}:{SENTIMENT_MODEL_SERVICE_PORT}"

EMOTION_MODEL_SERVICE_HOST = os.environ.get('EMOTION_MODEL_SERVICE_HOST', 'localhost')
EMOTION_MODEL_SERVICE_PORT = os.environ.get('EMOTION_MODEL_SERVICE_PORT', 8052)
EMOTION_MODEL_SERVICE_URL = f"http://{EMOTION_MODEL_SERVICE_HOST}:{EMOTION_MODEL_SERVICE_PORT}"

WORDCLOUD_SERVICE_HOST = os.environ.get('WORDCLOUD_SERVICE_HOST', '0.0.0.0')
WORDCLOUD_SERVICE_PORT = os.environ.get('WORDCLOUD_SERVICE_PORT', 8001)
WORDCLOUD_SERVICE_URL = f"http://{WORDCLOUD_SERVICE_HOST}:{WORDCLOUD_SERVICE_PORT}"


class API:
    def get_offline_data(self):
        import pandas as pd
        df = pd.read_csv("data.csv")
        return df.to_json(orient='records')        


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
    
    def get_wordcloud_from_text(self, text):
        body = {'input': text}
        request = requests.post(f"{WORDCLOUD_SERVICE_URL}/wordcloud/text", json=body)
        return request.json()['output']