
from tabs import *
from utils import *
from graphs import *
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, ctx
from streamApi import StreamerApiClient
from sentiment_api import ModelApiClient
import pandas as pd
import dash_bootstrap_components as dbc
from functions import *
from main import app
from Models.keyword_extraction_api import *
from Models.NER_api import *
from Models.emotion_api import *


streamer_api = StreamerApiClient()
model_api = ModelApiClient()
emotion_api = EmotionApiClient()

df = pd.read_json(streamer_api.get_offline_tweets())[:1000]


@app.callback(Output('my_interval', 'interval'), Input('refresh_rate', 'value'))
def set_interval(v):
    return float(v)*1000


interval = dcc.Interval(
    id='my_interval',
    disabled=False,
    interval=1000*6,
    n_intervals=0,
    max_intervals=-1,
)

card_count_tweets = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(children=f"{df.shape[0]}", id="tweets_count",
                       className="h2 font-weight-bold mb-0",
                       ),
                html.H6("No. of Tweets",
                        className="card-title text-uppercase text-muted mb-0"),

            ]
        ),
    ],
    class_name="card shadow",
)

card_users = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(children=f"{df['author_id'].nunique()}", id="users_count",
                       className="h2 font-weight-bold mb-0",
                       ),
                html.H6("No. of Users",
                        className="card-title text-uppercase text-muted mb-0"),

            ]
        ),
    ],
    class_name="card shadow",
)

card_positives = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(children=f"--", id="positives_count",
                       className="h2 font-weight-bold mb-0",
                       ),
                html.H6("No. of positive users",
                        className="card-title text-uppercase text-muted mb-0"),

            ]
        ),
    ],
    class_name="card shadow",
)

card_negatives = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(children=f"--", id="negatives_count",
                       className="h2 font-weight-bold mb-0",
                       ),
                html.H6("No. of negative users",
                        className="card-title text-uppercase text-muted mb-0"),

            ]
        ),
    ],
    class_name="card shadow",
)

trending_countries = {'United States': '23424977',
                      'United Kingdom': '23424975', 'Canada': '23424775', }
trending_countries = [dbc.Label("Select Country:", style={
    'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}), dcc.Dropdown(
    id='trending_countries', options=[{'label': k, 'value': v} for k, v in trending_countries.items()], value='23424977', style={'width': '70%'}, clearable=False, className="")]


button_refresh_predict = html.Div([dbc.Button("Predict", id="button-refresh-predict", className="button_predict", )])
refresh_predict = [html.Br(), dbc.Label("Make Prediction:", style={
    'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}), button_refresh_predict]

refresh_predict_spinner = dbc.Spinner(
    size="lg", color="light", type="border", fullscreen=False,)

refresh_rate = [html.Br(), dbc.Label("Refresh rate (sec):", style={
    'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}),
    dcc.Slider(
    id="refresh_rate",
    min=2,
    max=100,
    value=5,
    marks=None,
    className="", tooltip={"placement": "bottom", "always_visible": True},
), ]

stream_search = [html.Br(), dbc.Label("Topic to search:", style={
    'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}),
    dbc.Input(id="topic-input", type="text", placeholder="Enter topic",
              className="topic_input", style={'width': '40%'}),
    dbc.Button(children="Search",
               id="button-stream", className="button_predict", style={'width': '20%', 'font-size': '100%'}, )]

config_card = dbc.Card([
    dbc.CardHeader("Configure Dashboard", className="card-header"),
    dbc.CardBody([*trending_countries,
                  *refresh_predict,
                  *refresh_rate,
                  *stream_search,
                  ]),
],
    id='config_card',
    class_name="card shadow",
)


trend_graph = dcc.Graph(id='trend_graph', className='card shadow',)
sentiment_graph = dcc.Graph(id='sentiment_graph', className='card shadow',)
emotion_graph = dcc.Graph(id='emotion_graph', className='card shadow',)


tab_positive_word_cloud = dbc.Tab(
    label="Positive Word Cloud", tab_id="tab-positive-word-cloud", style={}, labelClassName="w-100")
tab_positive_word_count = dbc.Tab(
    label="Positive Word Count", tab_id="tab-positive-word-count", )

tab_negative_word_cloud = dbc.Tab(
    label="Negative Word Cloud", tab_id="tab-negative-word-cloud", style={}, labelClassName="w-100")
tab_negative_word_count = dbc.Tab(
    label="Negative Word Count", tab_id="tab-negative-word-count", )

positive_tabs = html.Div(dbc.Tabs(
    [tab_positive_word_cloud, tab_positive_word_count], id="positive_tab", active_tab='tab-positive-word-cloud', style={'background-color': "#1D262F"}), )

negative_tabs = html.Div(dbc.Tabs(
    [tab_negative_word_cloud, tab_negative_word_count], id="negative_tab", active_tab='tab-negative-word-cloud', style={'background-color': "#1D262F"},), )


store_stream_data = dcc.Store(id='store-stream-data', storage_type='memory')
store_sentiment_prediction = dcc.Store(
    id='store-sentiment-prediction', storage_type='memory')
store_emotion_prediction = dcc.Store(
    id='store-emotion-prediction', storage_type='memory')

card_kewords_word_cloud = dbc.Card([
    dbc.CardHeader(
        "Keywords", className="card-header", style={'position': 'center', 'color': '#8898aa'}),

    dbc.CardBody([
        html.Div(
            dbc.CardImg(id='keywords-wordcloud',), className="", style={'height': '500px'},
        )
    ], className=""),
],
    className="card shadow", )

card_ner_word_cloud = dbc.Card([
    dbc.CardHeader(
        "Entities", className="card-header", style={'position': 'center', 'color': '#8898aa'}),

    dbc.CardBody([
        html.Div(
            dbc.CardImg(id='ner-wordcloud',), className=""
        )
    ], className=""),
],
    className="card shadow",)

app.layout = html.Div(
    [interval, store_stream_data, store_sentiment_prediction, store_emotion_prediction,

        dbc.Row([
            dbc.Col(config_card, width=4),
            dbc.Col(children=[
                dbc.Row([
                    dbc.Col(card_count_tweets, width=3),
                    dbc.Col(card_users, width=3),
                    dbc.Col(card_positives, width=3),
                    dbc.Col(card_negatives, width=3),
                ]),

                html.Div(id='placeholder', style={'display': 'none'}),

                html.Div(
                    dbc.Row([
                        dbc.Col(html.Div([trend_graph],
                                className="card shadow"), width=12),
                    ]), className=""),
            ],
                width=8),

        ]),

     dbc.Row([
         dbc.Col(card_kewords_word_cloud, ),
         dbc.Col(card_ner_word_cloud, ),

     ],),

     dbc.Row([
         dbc.Col(html.Div(emotion_graph, className="card shadow"), width=6),
         dbc.Col(html.Div(sentiment_graph, className="card shadow"), width=6),

     ]),

        dbc.Row([

            dbc.Col(dbc.Row([
                negative_tabs,
                html.Div(id='negative-tab-content', children=[]),
            ],
            ), width=6),

            dbc.Col(dbc.Row([
                positive_tabs,
                html.Div(id='positive-tab-content', children=[]),
            ],
            ), width=6),
        ]),


     ])


@app.callback([Output('button-stream', 'children')], [Input('button-stream', 'n_clicks')], [State('topic-input', 'value')])
def start_stream(n, topic):
    if not topic:
        raise dash.exceptions.PreventUpdate
    if n % 2 == 1:
        streamer_api.start_stream(topic)
        return ["Stop"]
    else:
        streamer_api.stop_stream()
        return ["Start"]


@app.callback(Output('store-stream-data', 'data'), [Input('my_interval', 'n_intervals'), State('button-stream', 'n_clicks')])
def update_stream_data(n, n_clicks):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate
    isStreaming = n_clicks % 2 == 1
    if isStreaming:
        return streamer_api.get_tweets()
    else:
        raise dash.exceptions.PreventUpdate


@app.callback([
    Output("tweets_count", 'children'), Output('users_count', 'children'),
],
    [Input('store-stream-data', 'data')])
def update_count(data):
    df_stream = pd.read_json(data)
    return [str(df_stream.shape[0]), str(df_stream['author_id'].nunique())]

@app.callback([
    Output("positives_count", 'children'), Output('negatives_count', 'children'),
],
    [Input('store-sentiment-prediction', 'data')])
def update_positive_negative_user(data):
    df_sentiment = pd.DataFrame(data)
    df_positive = df_sentiment[df_sentiment['label'] == 'POSITIVE']
    df_negative = df_sentiment[df_sentiment['label'] == 'NEGATIVE']
    return [df_positive['author_id'].nunique(), df_negative['author_id'].nunique()]

@app.callback(Output('trend_graph', 'figure'),  [Input("trending_countries", "value"), State('trending_countries', 'options')])
def trend_graph(value, options):
    label = [x['label'] for x in options if x['value'] == value][0]
    df_trends = get_trends(value)
    return get_trends_graph(df_trends, label)


@app.callback([Output('store-sentiment-prediction', 'data'), Output('store-emotion-prediction', 'data'), Output('button-refresh-predict', 'n_clicks')],  [Input('button-refresh-predict', 'n_clicks')], [State('store-stream-data', 'data'), State('button-stream', 'n_clicks')], prevent_initial_call=False)
def make_prediction(refresh_button_clicks, data, stream_button_clicks):
    if not data:
        if not refresh_button_clicks:
            df_offline_tweets = df
            df_sentiment = form_sntiment_prediction_df(
                model_api.predict(df_offline_tweets))
            df_emotion = form_emotion_prediction_df(
                emotion_api.predict(df_offline_tweets))
            return [df_sentiment.to_dict('records'), df_emotion.to_dict('records'), refresh_button_clicks]
        else:
            raise dash.exceptions.PreventUpdate
    else:
        isStreaming = stream_button_clicks % 2 == 1
        if isStreaming:
            n_clicks = 0
            df_stream = pd.read_json(data)
            df_sentiment = form_sntiment_prediction_df(
                model_api.predict(df_stream))
            df_emotion = form_emotion_prediction_df(
                emotion_api.predict(df_stream))
            return [df_sentiment.to_dict('records'), df_emotion.to_dict('records'), n_clicks]
        else:
            if refresh_button_clicks == 1:
                df_stream = pd.read_json(data)
                df_sentiment = form_sntiment_prediction_df(
                    model_api.predict(df_stream))
                df_emotion = form_emotion_prediction_df(
                    emotion_api.predict(df_stream))
                return [df_sentiment.to_dict('records'), df_emotion.to_dict('records'), refresh_button_clicks]
            else:
                raise dash.exceptions.PreventUpdate


@app.callback(Output('sentiment_graph', 'figure'),  [Input('store-sentiment-prediction', 'data'), ], prevent_initial_call=False)
def make_sentiment_graph(data, ):
    sentiment_count = get_label_count(data)
    return get_sentiment_graph(sentiment_count)


@app.callback(Output('emotion_graph', 'figure'),  [Input('store-emotion-prediction', 'data'), ], prevent_initial_call=False)
def make_emotion_graph(data, ):
    emotion_count = get_label_count(data)
    return get_emotion_graph(emotion_count)


@app.callback(
    Output("negative-tab-content", "children"),
    [Input("negative_tab", "active_tab")]
)
def switch_negative_tab(active_tab):
    if active_tab == "tab-negative-word-cloud":
        return layout_negative_wordcloud
    elif active_tab == "tab-negative-word-count":
        return layout_grapth_negative_word_count


@app.callback(
    Output("positive-tab-content", "children"),
    [Input("positive_tab", "active_tab")]
)
def switch_positive_tab(active_tab):
    if active_tab == "tab-positive-word-cloud":
        return layout_positive_wordcloud
    elif active_tab == "tab-positive-word-count":
        return layout_grapth_positive_word_count


@app.callback(Output('keywords-wordcloud', 'src'), Input('store-stream-data', 'data'), Input('button-stream', 'n_clicks'))
def get_keywords(data, stream_button_clicks):
    if not stream_button_clicks:
        df_stream = df
    else:
        df_stream = pd.read_json(data)
    img = BytesIO()
    keywords = extract_keywords(df_stream['text'])['keywords']
    make_wordcloud(" ".join(keywords), 810, 500).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


@app.callback(Output('ner-wordcloud', 'src'), Input('store-stream-data', 'data'), Input('button-stream', 'n_clicks'))
def get_ents(data, stream_button_clicks):
    if not stream_button_clicks:
        df_stream = df
    else:
        df_stream = pd.read_json(data)
    img = BytesIO()
    ents = get_ner(df_stream['text'])['entities']
    make_wordcloud(" ".join(ents), 810, 500).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


if __name__ == '__main__':
    app.run_server(debug=True, port='7020')
