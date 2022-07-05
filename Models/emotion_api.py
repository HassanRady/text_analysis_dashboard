

import requests


class EmotionApiClient:
    def predict(self, df):
        X = df['text']

        body = {'inputs': X.tolist()}
        request = requests.post('http://localhost:8502/v1/models/emotion/versions/1:predict', json=body)
        request_json = request.json()
        request_json['tweet'] = X
        request_json['author_id'] = df['author_id']

        return request_json












