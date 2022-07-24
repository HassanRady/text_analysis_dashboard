import pandas as pd
from collections import Counter
from api_callbacks import APICallbacks

api_services = APICallbacks()

def get_trends(value):
    df_trends = pd.read_json(api_services.get_trending_hashtags(int(value)))
    df_trends = df_trends[['name', 'tweet_volume']]
    df_trends = df_trends.sort_values(by='tweet_volume', ascending=False)
    df_trends = df_trends.head(10)
    return df_trends

def get_label_count(data, col='label'):
    df = pd.DataFrame(data)
    label_count = df[col].value_counts()
    return label_count

def get_sentiment_word_count(data, sentiment):
    df_sentiment = pd.DataFrame(data)
    df = df_sentiment.query(f"label == '{sentiment}'")
    return df.tweet.str.split(expand=True).stack().value_counts()

