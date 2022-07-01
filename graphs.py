from tabs import *
from utils import *
from io import BytesIO
import base64
from graphs import *
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from functions import *
from main import app
from plotly import graph_objs as go
from main import app


def get_sentiment_graph(label_count):
    
    def __get_color(label):
        if label == 'POSITIVE':
            return '#00d1ff'
        elif label == 'NEGATIVE':
            return '#ff4a55'
        else:
            return '#33ffe6'

    data = [go.Pie(hole=0.6,
            labels=label_count.index,
            values=label_count,
            marker=dict(
                colors=[__get_color(label)
                        for label in label_count.index],
            ),
            text=[l for l in label_count.index],
            textposition='auto',
            )]

    layout = go.Layout(
        title='Sentiment Percentage',
        plot_bgcolor='#1D262F',
        paper_bgcolor='#1D262F',
        font=dict(
            family='Open Sans, sans-serif',
            size=12,
            color='#7f7f7f',
        ),
        autosize=True,
        grid=dict(
        ),
        modebar=dict(orientation='v'),
        xaxis=dict(color='#8898aa',),
        yaxis=dict(color='#8898aa', gridwidth=1, gridcolor='#5C8CBE'),


    )
    layout.titlefont = dict(size=24, color='#8898aa',
                            family='Open Sans, sans-serif')
    return {'data': data, 'layout': layout}



def get_emotion_graph(label_count):
    
    def __get_color(label):
        if label == 'joy':
            return '#00d1ff'
        elif label == 'sadness':
            return '#ff4a55'
        elif label == 'anger':
            return '#33ffe6'
        elif label == 'fear':
            return '#ff4a55'
        elif label == 'surprise':
            return '#33ffe6'
        elif label == 'love':
            return '#00d1ff'

    data = [go.Pie(hole=0.6,
            labels=label_count.index,
            values=label_count,
            marker=dict(
                colors=[__get_color(label)
                        for label in label_count.index],
            ),
            text=[l for l in label_count.index],
            textposition='auto',
            )]

    layout = go.Layout(
        title='Emotion Percentage',
        plot_bgcolor='#1D262F',
        paper_bgcolor='#1D262F',
        font=dict(
            family='Open Sans, sans-serif',
            size=12,
            color='#7f7f7f',
        ),
        autosize=True,
        grid=dict(
        ),
        modebar=dict(orientation='v'),
        xaxis=dict(color='#8898aa',),
        yaxis=dict(color='#8898aa', gridwidth=1, gridcolor='#5C8CBE'),


    )
    layout.titlefont = dict(size=24, color='#8898aa',
                            family='Open Sans, sans-serif')
    return {'data': data, 'layout': layout}


def get_trends_graph(df_trends, label):
    data = [go.Bar(
            x=df_trends['name'],
            y=df_trends['tweet_volume'],
            text=df_trends['tweet_volume'],
            textposition='auto',
            marker=dict(
                color='#00d1ff',
            ),
            )]

    layout = go.Layout(
        title=f'Top 10 Trending Hashtags ({label})',
        plot_bgcolor='#1D262F',
        paper_bgcolor='#1D262F',
        font=dict(
            family='Open Sans, sans-serif',
            size=12,
            color='#7f7f7f',
        ),
        autosize=True,
        grid=dict(
        ),
        modebar=dict(orientation='v'),
        xaxis=dict(color='#8898aa',),
        yaxis=dict(color='#8898aa', gridwidth=1, gridcolor='#5C8CBE'),


    )
    layout.titlefont = dict(size=24, color='#8898aa',
                            family='Open Sans, sans-serif')
    return {'data': data, 'layout': layout}



def make_graph_negative_word_count(data):
    X = data[:10]
    x = X.index
    y = X.values
    data = [go.Bar(
            x=x,
            y=y,
            text=y,
            textposition='auto',
            marker=dict(
                color='#00d1ff',
            ),
            )]

    layout = go.Layout(
        title='Negative Word Count',
        plot_bgcolor='#1D262F',
        paper_bgcolor='#1D262F',
        font=dict(
            family='Open Sans, sans-serif',
            size=12,
            color='#7f7f7f',
        ),
        autosize=True,
        grid=dict(
        ),
        modebar=dict(orientation='v'),
        xaxis=dict(color='#8898aa',),
        yaxis=dict(color='#8898aa', gridwidth=1, gridcolor='#5C8CBE'),


    )
    layout.titlefont = dict(size=24, color='#8898aa',
                            family='Open Sans, sans-serif')
    return {'data': data, 'layout': layout}

def make_graph_positive_word_count(data):
    X = data[:10]
    x = X.index
    y = X.values
    data = [go.Bar(
            x=x,
            y=y,
            text=y,
            textposition='auto',
            marker=dict(
                color='#00d1ff',
            ),
            )]

    layout = go.Layout(
        title='Positive Word Count',
        plot_bgcolor='#1D262F',
        paper_bgcolor='#1D262F',
        font=dict(
            family='Open Sans, sans-serif',
            size=12,
            color='#7f7f7f',
        ),
        autosize=True,
        grid=dict(
        ),
        modebar=dict(orientation='v'),
        xaxis=dict(color='#8898aa',),
        yaxis=dict(color='#8898aa', gridwidth=1, gridcolor='#5C8CBE'),


    )
    layout.titlefont = dict(size=24, color='#8898aa',
                            family='Open Sans, sans-serif')
    return {'data': data, 'layout': layout}