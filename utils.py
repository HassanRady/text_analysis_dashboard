
# Python program to generate WordCloud

# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
from PIL import Image
import numpy as np


stopwords = set(STOPWORDS)
stopwords.update(['RT', 'https', 'user', '@'])

def make_sentiment_wordcloud(df_preds, sentiment):

    sentiment_tweets = df_preds[df_preds['label'] == sentiment]
    tweets = sentiment_tweets['tweet'].tolist()
    text = " ".join(tweets)

    mask = np.array(Image.open("twitter2.png"))
    wordcloud = WordCloud(stopwords=stopwords, background_color="#1D262F",
                        max_words=1000, mask=mask, contour_color='yellow', random_state=42, ).generate(text)
    return wordcloud.to_image()
