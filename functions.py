import pandas as pd
from streamApi import StreamerApiClient
from collections import Counter

streamer_api = StreamerApiClient()


def get_trends(value):
    df_trends = pd.read_json(streamer_api.get_trending_hashtags(int(value)))
    df_trends = df_trends[['name', 'tweet_volume']]
    df_trends = df_trends.sort_values(by='tweet_volume', ascending=False)
    df_trends = df_trends.head(10)
    return df_trends

def get_sentiment_count(data):
    df_sentiment = pd.DataFrame(data)
    sentiment_count = df_sentiment['label'].value_counts()
    return sentiment_count

def get_sentiment_word_count(data, sentiment):
    df_sentiment = pd.DataFrame(data)
    df = df_sentiment.query(f"label == '{sentiment}'")
    return df.tweet.str.split(expand=True).stack().value_counts()

