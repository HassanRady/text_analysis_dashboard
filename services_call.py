import requests
from config import settings


class Services:    
    @staticmethod
    def get_wordcloud_from_text(text):
        body = {'input': text}
        request = requests.post(settings.WORDCLOUD_SERVICE_URL, json=body)
        return request.json()
    
    @staticmethod
    def get_subreddit_trends():
        request = requests.get(settings.TREND_SUBREDDIT_SERVICE_URL)
        return request.json()