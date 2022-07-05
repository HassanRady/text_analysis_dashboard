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
from graphs import *

layout_negative_wordcloud = html.Div([
    html.Img(id='negative-wordcloud',),
], className="card shadow", style={'margin':'0px 0px 0px 0px'})


@app.callback(Output('negative-wordcloud', 'src'),  [Input('store-sentiment-prediction', 'data'), ], prevent_initial_call=False, )
def call_negative_wordcloud(data, ):
    img = BytesIO()
    df_sentiment = pd.DataFrame(data)
    make_sentiment_wordcloud(df_sentiment, "NEGATIVE").save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


layout_grapth_negative_word_count = dcc.Graph(id='negative-word-count',)


@app.callback(Output('negative-word-count', 'figure'), Input('store-sentiment-prediction', 'data'), prevent_initial_call=False, )
def tab_grapth_negative_word_count(data):
    data = get_sentiment_word_count(data, "NEGATIVE")
    return make_graph_negative_word_count(data)


refresh_predict_spinner =  dbc.Spinner( children=html.Img(id='positive-wordcloud',) ,size="lg", color="light", type="border", fullscreen=False,)

layout_positive_wordcloud = html.Div([
    html.Img(id='positive-wordcloud',), 
# refresh_predict_spinner
], className="card shadow", style={'margin':'0px 0px 0px 0px'})

layout_positive_wordcloud = html.Div([layout_positive_wordcloud],
    className="", style={'margin':'0px 0px 0px 0px'}
)


@app.callback(Output('positive-wordcloud', 'src'),  [Input('store-sentiment-prediction', 'data'), ], prevent_initial_call=False, )
def call_positive_wordcloud(data, ):
    img = BytesIO()
    df_sentiment = pd.DataFrame(data)
    make_sentiment_wordcloud(df_sentiment, "POSITIVE").save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


layout_grapth_positive_word_count = dcc.Graph(id='positive-word-count',)


@app.callback(Output('positive-word-count', 'figure'), Input('store-sentiment-prediction', 'data'), prevent_initial_call=False, )
def tab_grapth_positive_word_count(data):
    data = get_sentiment_word_count(data, "POSITIVE")
    return make_graph_positive_word_count(data)