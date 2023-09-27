import pandas as pd

def get_label_count(data, col='label'):
    df = pd.DataFrame(data)
    label_count = df[col].value_counts()
    return label_count

def get_sentiment_word_count(data, sentiment):
    df_sentiment = pd.DataFrame(data)
    df = df_sentiment.query(f"label == '{sentiment}'")
    return df.text.str.split(expand=True).stack().value_counts()

