

from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import re
import pandas as pd
from PIL import Image
import numpy as np
import base64
from io import BytesIO

from logger import get_file_logger


_logger = get_file_logger(__name__, 'debug')

stopwords = set(STOPWORDS)
stopwords.update(['RT', 'https', 'user', '@'])

NEGATIVE = "NEGATIVE"
POSITIVE = "POSITIVE"
NEUTRAL = "NEUTRAL"
NEUTRAL_THRESHOLD = 0.6


def get_final_sentiment_label(label, proba):
    return NEUTRAL if proba < NEUTRAL_THRESHOLD else label


def process_model_prediction_to_df(data):
    df = pd.DataFrame(data)
    df['outputs'] = df['outputs'].apply(lambda x: np.argmax(eval(str(x))))
    return df


classes = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']
classes_to_index = dict((c, i) for i, c in enumerate(classes))
index_to_classes = dict((v, k) for k, v in classes_to_index.items())


def interpret_emotion_prediction(x):
    return index_to_classes[x]


def form_redis_emotion_prediction_to_df(data):
    df = process_model_prediction_to_df(data)
    df['label'] = df['outputs'].apply(interpret_emotion_prediction)
    return df


def read_sentiment_model_prediction(data):
    df = pd.DataFrame(data)
    df['outputs'] = df['outputs'].apply(lambda x: x[0][0])
    return df


def interpret_sentiment_prediction(x):
    label = NEGATIVE if x < 0.5 else POSITIVE
    if label == NEGATIVE:
        negative_percent = 1-x
        positive_percent = x
        label = get_final_sentiment_label(label, negative_percent)
    else:
        positive_percent = (x - 0.5)/(0.5)
        negative_percent = 1-positive_percent
        label = get_final_sentiment_label(label, positive_percent)
    return label, negative_percent, positive_percent


def from_redis_sentiment_prediction_to_df(data):
    df = read_sentiment_model_prediction(data)
    df['label'], df['negative'], df['positive'] = zip(
        *df['outputs'].apply(interpret_sentiment_prediction))
    return df

def get_sentiment_text(df_preds, sentiment):
    sentiment_instances = df_preds[df_preds['label'] == sentiment]
    instances = sentiment_instances['text'].tolist()
    return " ".join(instances)

def process_redis_output_for_wordcloud(output: dict):
    df = pd.DataFrame(output)
    df['output'] = df['output'].astype(str)
    df['output'] = df['output'].str.replace("[", '', regex=True)
    df['output'] = df['output'].str.replace("]", '',regex=True)
    df['output'] = df['output'].str.replace(",", '',regex=True)
    return df['output'].str.cat()


if __name__ == "__main__":
    from config import settings
    from redis_handler import RedisClient

    print(from_redis_sentiment_prediction_to_df(RedisClient().get_data_from_list(settings.KAFKA_SENTIMENT_TOPIC)))