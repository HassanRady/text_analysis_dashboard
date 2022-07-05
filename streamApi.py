import requests
import json


class StreamerApiClient:
    def start_stream(self, topic):
        def _start_stream(topic):
            s = requests.get(
                "http://127.0.0.1:9000/start_stream", params={"topic": topic})
            s2 = requests.get(
            "http://127.0.0.1:9001/start", params={"topic": topic})
        _start_stream(topic)

    def stop_stream(self):
        response = requests.get("http://127.0.0.1:9000/stop_stream")
        response = requests.get("http://127.0.0.1:9001/stop")
        return response.text

    def get_tweets(self, ):
        response = requests.get(
            "http://127.0.0.1:9001/stream",)
        return response.json()


    def get_offline_tweets(self):
        response = requests.get(
            "http://127.0.0.1:9001/offline_tweets", )
        return response.json()

    def get_trending_hashtags(self, WOEID=1):
        response = requests.get("http://127.0.0.1:9011/trending_hashtags", params={f'WOEID': WOEID})
        return response.json()


    
