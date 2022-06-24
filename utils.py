
# Python program to generate WordCloud

# importing all necessary modules
from cmath import e
from tkinter import N
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
from PIL import Image
import numpy as np


stopwords = set(STOPWORDS)
stopwords.update(['RT', 'https', 'user', '@'])

NEGATIVE = "NEGATIVE"
POSITIVE = "POSITIVE"
NEUTRAL = "NEUTRAL"
NEUTRAL_THRESHOLD = 0.6

def get_final_label(label, proba):
        if proba < NEUTRAL_THRESHOLD:
            return NEUTRAL
        else:
            return label


def read_model_prediction(data):
    df = pd.DataFrame(data)
    df['outputs'] = df['outputs'].apply(lambda x: x[0])
    return df


def interpret_prediction(x):
    label = NEGATIVE if x < 0.5 else POSITIVE
    if label == NEGATIVE:
        negative_percent = 1-x
        positive_percent = x
        label = get_final_label(label, negative_percent)
    else:
        positive_percent = (x - 0.5)/(0.5)
        negative_percent = 1-positive_percent
        label = get_final_label(label, positive_percent)
    return label, negative_percent, positive_percent

def form_sntiment_prediction_df(data):
    df = read_model_prediction(data)
    df['label'], df['negative'], df['positive'] = zip(*df['outputs'].apply(interpret_prediction))
    return df


def make_sentiment_wordcloud(df_preds, sentiment):

    sentiment_tweets = df_preds[df_preds['label'] == sentiment]
    tweets = sentiment_tweets['tweet'].tolist()
    text = " ".join(tweets)

    mask = np.array(Image.open("twitter2.png"))
    wordcloud = WordCloud(stopwords=stopwords, background_color="#1D262F",
                        max_words=1000, mask=mask, contour_color='yellow', random_state=42, ).generate(text)
    return wordcloud.to_image()

def make_wordcloud(text):
    wordcloud = WordCloud(stopwords=stopwords, background_color="#1D262F",
                        max_words=1000, random_state=42, ).generate(text)
    return wordcloud.to_image()
