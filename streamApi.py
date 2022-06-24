import requests
import json


class StreamerApiClient:
    def start_stream(self, topic, stop=True):
        def _start_stream(topic):
            s = requests.get(
                "http://127.0.0.1:9000/start_stream", params={"topic": topic})
        _start_stream(topic)

    def stop_stream(self):
        response = requests.get("http://127.0.0.1:9000/stop_stream")
        return response.text

    def get_tweets(self, wait=4):
        response = requests.get(
            "http://127.0.0.1:9000/tweets_stream", params={f'wait': wait})
        return response.json()

    def clean_tweets(self, wait=4):
        response = requests.get(
            "http://127.0.0.1:9000/clean", params={f'wait': wait})
        return response

    def get_word_count(self, wait=4):
        response = requests.get(
            "http://127.0.0.1:9000/wordCount", params={f'wait': wait})
        return response.json()

    def get_offline_tweets(self, topic=None):
        response = requests.get(
            "http://127.0.0.1:9000/offline_tweets", params={f'topic': topic})
        return response.json()

    def get_trending_hashtags(self, WOEID=1):
        response = requests.get("http://127.0.0.1:9000/trending_hashtags", params={f'WOEID': WOEID})
        return response.json()

    def offline_word_count(self, topic=None):
        response = requests.get(
            "http://127.0.0.1:9000/offline_word_count", params={f'topic': topic})
        return response.json()

    
