import requests


class ModelApiClient:
    def predict(self, X):
        body = {'inputs': X.tolist()}
        request = requests.post('http://localhost:8501/v1/models/tweet-sentiment:predict', json=body)
        request_json = request.json()
        request_json['tweet'] = X
        return request_json