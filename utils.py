

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

def read_emotion_model_prediction(data):
    df = pd.DataFrame(data)
    df['outputs'] = df['outputs'].apply(lambda x: np.argmax(x))
    return df

classes = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']
classes_to_index = dict((c, i) for i, c in enumerate(classes))
index_to_classes = dict((v, k) for k, v in classes_to_index.items())

def interpret_emotion_prediction(x):
        return index_to_classes[x]

def form_emotion_prediction_df(data):
    df = read_emotion_model_prediction(data)
    df['label'] = df['outputs'].apply(interpret_emotion_prediction)
    return df

def read_sentiment_model_prediction(data):
    df = pd.DataFrame(data)
    df['outputs'] = df['outputs'].apply(lambda x: x[0])
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

def form_sntiment_prediction_df(data):
    df = read_sentiment_model_prediction(data)
    df['label'], df['negative'], df['positive'] = zip(*df['outputs'].apply(interpret_sentiment_prediction))
    return df


def make_sentiment_wordcloud(df_preds, sentiment):

    sentiment_instances = df_preds[df_preds['label'] == sentiment]
    instances = sentiment_instances['text'].tolist()
    text = " ".join(instances)

    mask = np.array(Image.open("reddit.png"))
    wordcloud = WordCloud(stopwords=stopwords, background_color="#1D262F",
                        max_words=1000, mask=mask, contour_color='yellow', random_state=42, colormap='tab20c',).generate(text)
    return wordcloud.to_image()

def get_word_frequency(text):
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

import time
wordcloud = WordCloud(stopwords=stopwords, background_color="#1D262F",
                        random_state=42, height=810, width=500,  colormap='tab20c',)
def get_wordcloud(word_freq):
    img = BytesIO()    
    start = time.time()
    gen_cloud = wordcloud.generate_from_frequencies(word_freq)
    print(f"Time taken to generate wordcloud: {time.time() - start}")
    gen_cloud.to_image().save(img, format='PNG')
    return f"data:image/png;base64, {base64.b64encode(img.getvalue()).decode()}"


