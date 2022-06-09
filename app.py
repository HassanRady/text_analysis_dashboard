
from utils import *
from io import BytesIO
import base64
from graphs import *
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, dash_table
from ApiClient import StreamerApiClient, ModelApiClient
import pandas as pd
import dash_bootstrap_components as dbc
from functions import *

from plotly import graph_objs as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
streamer_api = StreamerApiClient()
model_api = ModelApiClient()

df = pd.read_json(streamer_api.get_offline_tweets())[
    ['text', 'name', 'screen_name', 'location', 'topic', 'user_id']]
df_show = df.copy().drop(columns=['user_id'])


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
                html.P(children=f"{df_show.shape[0]}", id="tweets_count",
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
                html.P(children=f"{df['user_id'].nunique()}", id="users_count",
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
                html.P(f"{df['user_id'].nunique()}", id="positives_count",
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
                html.P(f"{df['user_id'].nunique()}", id="negatives_count",
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
dropdown_trending_countries = dcc.Dropdown(
    id='dropdown-trending-countries', options=[{'label': k, 'value': v} for k, v in trending_countries.items()], value='23424977', style={'width': '70%'}, clearable=False)

button_refresh_predict = dbc.Button("", id="button-refresh-predict", className="glyphicon glyphicon-refresh",
                                    style={'width': '20%', 'font-size': '100%'}, color="light")
config_card = dbc.Card([
    dbc.CardHeader("Configure Dashboard", className="card-header"),
    dbc.CardBody([dropdown_trending_countries, button_refresh_predict,
                  dbc.Form([
                      dbc.Label("Topic to search:", style={
                          'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}),
                      dbc.Input(id="topic-input", type="text", placeholder="Enter topic",
                                className="", style={'width': '40%'}),
                      dbc.Label("Refresh rate:", style={
                                'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}),
                      dcc.Slider(
                          id="refresh_rate",
                          min=6,
                          max=100,
                          value=6,
                          className="",
                      ),
                      dbc.Button(children="Search",
                                 id="button-stream", color="primary",),


                  ],),
                  ]),
],
    id='config_card',
    class_name="card shadow",
)


trend_graph = dcc.Graph(id='trend_graph', className='card shadow',)
sentiment_graph = dcc.Graph(id='sentiment_graph', className='card shadow',)
negative_word_cloud = dcc.Graph(
    id='negative_word_cloud', className='card shadow',)
positive_word_cloud = dcc.Graph(
    id='positive_word_cloud', className='card shadow',)

store_stream_data = dcc.Store(id='store-stream-data', storage_type='memory')
store_sentiment_prediction = dcc.Store(
    id='store-sentiment-prediction', storage_type='memory')

negative_wordcloud = html.Div([html.P("Negative Word Cloud",
                                      className="", style={'margin': '0.5em', 'text-align': 'center', 'color': '#8898aa', 'family': 'Open Sans, sans-serif', 'font-size': '1.5em'}),
                               html.Img(id='negative-wordcloud',),
                               ], className="card shadow")


positive_wordcloud = html.Div([html.P("Positive Word Cloud",
                                      className="", style={'margin': '0.5em', 'text-align': 'center', 'color': '#8898aa', 'family': 'Open Sans, sans-serif', 'font-size': '1.5em'}),
                               html.Img(id='positive-wordcloud',),
                               ], className="card shadow")


app.layout = html.Div(
    [interval, store_stream_data, store_sentiment_prediction,

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
            dbc.Col(html.Div(sentiment_graph, className="card shadow"), width=4),
            dbc.Col(negative_wordcloud,
                    width=4),
            dbc.Col(positive_wordcloud,
                    width=4),
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
        return streamer_api.get_tweets(wait=0)
    else:
        raise dash.exceptions.PreventUpdate


@app.callback([
    Output("tweets_count", 'children'), Output('users_count', 'children'),
],
    [Input('store-stream-data', 'data')])
def update_count(data):
    df_stream = pd.read_json(data)
    return [str(df_stream.shape[0]), str(df_stream['user_id'].nunique())]


@app.callback(Output('trend_graph', 'figure'),  [Input("dropdown-trending-countries", "value"), State('dropdown-trending-countries', 'options')])
def trend_graph(value, options):
    label = [x['label'] for x in options if x['value'] == value][0]
    df_trends = get_trends(value)
    return get_trends_graph(df_trends, label)


@app.callback([Output('store-sentiment-prediction', 'data'), Output('button-refresh-predict', 'n_clicks')],  [Input('button-refresh-predict', 'n_clicks')], [State('store-stream-data', 'data'), State('button-stream', 'n_clicks')], prevent_initial_call=False)
def placeholder(refresh_button_clicks, data, stream_button_clicks):
    if not data:
        if not refresh_button_clicks:
            df_offline_tweets = pd.read_json(streamer_api.get_offline_tweets())
            df_sentiment = pd.read_json(
                model_api.predict(df_offline_tweets['text']))
            return [df_sentiment.to_dict('records'), refresh_button_clicks]
        else:
            raise dash.exceptions.PreventUpdate
    else:
        isStreaming = stream_button_clicks % 2 == 1
        if isStreaming:
            n_clicks = 0
            df_stream = pd.read_json(data)
            df_sentiment = pd.read_json(model_api.predict(df_stream['text']))
            return [df_sentiment.to_dict('records', ), n_clicks]
        else:
            if refresh_button_clicks == 1:
                df_stream = pd.read_json(data)
                df_sentiment = pd.read_json(
                    model_api.predict(df_stream['text']))
                return [df_sentiment.to_dict('records'), refresh_button_clicks]
            else:
                raise dash.exceptions.PreventUpdate


@app.callback(Output('sentiment_graph', 'figure'),  [Input('store-sentiment-prediction', 'data')], prevent_initial_call=False)
def sentiment_graph(data):
    sentiment_count = get_sentiment_count(data)
    return get_sentiment_graph(sentiment_count)


@app.callback(Output('negative-wordcloud', 'src'),  [Input('store-sentiment-prediction', 'data')], prevent_initial_call=False)
def negative_wordcloud(data):
    img = BytesIO()
    df_sentiment = pd.DataFrame(data)
    make_sentiment_wordcloud(df_sentiment, "NEGATIVE").save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


@app.callback(Output('positive-wordcloud', 'src'),  [Input('store-sentiment-prediction', 'data')], prevent_initial_call=False)
def positive_wordcloud(data):
    img = BytesIO()
    df_sentiment = pd.DataFrame(data)
    make_sentiment_wordcloud(df_sentiment, "POSITIVE").save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


if __name__ == '__main__':
    app.run_server(debug=True, port='7020')
