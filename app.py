from tabs import *
from utils import *
from graphs import *
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, ctx
import pandas as pd
import dash_bootstrap_components as dbc
from functions import *
from main import app
from services_call import Services
from redis_handler import RedisClient

from logger import get_file_logger

from config import settings


_logger = get_file_logger(__name__)

services_client = Services()
redis_client = RedisClient()


refresh_rate_value = 10
MILLISECOND_IN_SECOND= 1000


@app.callback(Output('my_interval', 'interval'), Input('refresh_rate', 'value'))
def set_interval(v):
    return float(v)*MILLISECOND_IN_SECOND


hidden_div = html.Div(id='placeholder', style={'display': 'none'})


interval = dcc.Interval(
    id='my_interval',
    disabled=False,
    interval=MILLISECOND_IN_SECOND*refresh_rate_value,
    n_intervals=0,
    max_intervals=-1,
)

# card_count_instances = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.P(children=f"{df.shape[0]}", id="instance_count",
#                        className="h2 font-weight-bold mb-0",
#                        ),
#                 html.H6("No. of Instances",
#                         className="card-title text-uppercase text-muted mb-0"),
#             ]
#         ),
#     ],
#     class_name="card shadow",
# )

# card_users = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.P(children=f"{df['author_id'].nunique()}", id="users_count",
#                        className="h2 font-weight-bold mb-0",
#                        ),
#                 html.H6("No. of Users",
#                         className="card-title text-uppercase text-muted mb-0"),

#             ]
#         ),
#     ],
#     class_name="card shadow",
# )

# card_positives = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.P(children=f"--", id="positives_count",
#                        className="h2 font-weight-bold mb-0",
#                        ),
#                 html.H6("No. of positive users",
#                         className="card-title text-uppercase text-muted mb-0"),

#             ]
#         ),
#     ],
#     class_name="card shadow",
# )

# card_negatives = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.P(children=f"--", id="negatives_count",
#                        className="h2 font-weight-bold mb-0",
#                        ),
#                 html.H6("No. of negative users",
#                         className="card-title text-uppercase text-muted mb-0"),

#             ]
#         ),
#     ],
#     class_name="card shadow",
# )

# trending_countries = {'United States': '23424977',
#                       'United Kingdom': '23424975', 'Canada': '23424775', }
# trending_countries = [dbc.Label("Select Country:", style={
#     'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}), dcc.Dropdown(
#     id='trending_countries', options=[{'label': k, 'value': v} for k, v in trending_countries.items()], value='23424977', style={'width': '70%'}, clearable=False, className="")]

# button_refresh_predict = html.Div(
#     [dbc.Button("Predict", id="button-refresh-predict", className="button_predict", )])
# refresh_predict = [html.Br(), dbc.Label("Make Prediction:", style={
#     'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}), button_refresh_predict]

# refresh_predict_spinner = dbc.Spinner(
#     size="lg", color="light", type="border", fullscreen=False,)


refresh_rate = [html.Br(), dbc.Label("Refresh rate (sec):", style={
    'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}),
    dcc.Slider(
    id="refresh_rate",
    min=2,
    max=100,
    value=refresh_rate_value,
    marks=None,
    className="", tooltip={"placement": "bottom", "always_visible": True},
), ]


stream_search = [html.Br(), dbc.Label("Topic to search:", style={
    'margin': '0.5em', 'color': '#8898aa', 'font-size': '1em'}),
    dbc.Input(id="topic-input", type="text", placeholder="Enter topic",
              className="topic_input", style={'width': '40%'}),
    dbc.Button(children="Search",
               id="button-stream", className="button_predict", style={'width': '20%', 'font-size': '100%'}, )]

# loading_spinner = html.Div(
#     [
#         # *refresh_predict,
#         dbc.Spinner(html.Div(id="loading-output")),
#     ]
# )

config_card = dbc.Card([
    dbc.CardHeader("Configure Dashboard", className="card-header"),
    dbc.CardBody([
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


store_sentiment_prediction = dcc.Store(
    id='store-sentiment-prediction', storage_type='memory')
store_emotion_prediction = dcc.Store(
    id='store-emotion-prediction', storage_type='memory')

card_keywords_word_cloud = dbc.Card([
    dbc.CardHeader(
        "Keywords", className="card-header", style={'position': 'center', 'color': '#8898aa'}),

    dbc.CardBody([
        html.Div(
            dbc.CardImg(id='keywords-wordcloud',), className="", style={'height': '510px'},
        )
    ], className=""),
],
    className="card shadow", )

card_ner_word_cloud = dbc.Card([
    dbc.CardHeader(
        "Entities", className="card-header", style={'position': 'center', 'color': '#8898aa'}),

    dbc.CardBody([
        html.Div(
            dbc.CardImg(id='ner-wordcloud',), className="", style={'height': '510px'}
        )
    ], className=""),
],
    className="card shadow",)

app.layout = html.Div([interval,
     dbc.Row([
         dbc.Col(card_keywords_word_cloud, ),
         dbc.Col(card_ner_word_cloud, ),

     ],),])

app.layout = html.Div(
    [hidden_div, interval, store_sentiment_prediction, store_emotion_prediction,

        dbc.Row([
            dbc.Col(config_card, width=4),
            dbc.Col(children=[
                # dbc.Row([
                    # dbc.Col(card_count_instances, width=3),
                    # dbc.Col(card_users, width=3),
                    # dbc.Col(card_positives, width=3),
        #             dbc.Col(card_negatives, width=3),
        #         ]),

                html.Div(
                    dbc.Row([
                        dbc.Col(html.Div([trend_graph],
                                className="card shadow"), width=12),
                    ]), className=""),
            ],
                width=8),

        ]),

     dbc.Row([
         dbc.Col(card_keywords_word_cloud, ),
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


# @app.callback([Output('button-stream', 'children'), Output("my_interval", "disabled")], [Input('button-stream', 'n_clicks')], [State('topic-input', 'value'), State("my_interval", "disabled")])
# def start_stream(n, topic, disabled):
#     if not topic:
#         raise dash.exceptions.PreventUpdate
#     if n % 2 == 1:
#         services_client.start_stream(topic)
#         redis_client.set_key('stream', 1)
#         redis_client.set_key('isStreamed', 1)
#         if topic != redis_client.get_key('topic') and topic != '':
#             redis_client.delete_stream_data()
#         redis_client.set_key('topic', topic)
#         return ["Stop", disabled]
#     else:
#         services_client.stop_stream()
#         redis_client.set_key('stream', 0)
#         return ["Start", not disabled]


# @app.callback([
#     Output("instance_count", 'children'), Output('users_count', 'children'),
# ],
#     [Input('my_interval', 'n_intervals')])
# def update_count(n):
#     isStreamed = redis_client.get_key("isStreamed") is not None
#     if isStreamed:
#         df_stream = redis_client.get_stream_data()
#     else:
#         df_stream = df
#     return [str(df_stream.shape[0]), str(df_stream['author_id'].nunique())]


# @app.callback([
#     Output("positives_count", 'children'), Output(
#         'negatives_count', 'children'),
# ],
#     [Input('store-sentiment-prediction', 'data')])
# def update_positive_negative_user(data):
#     df_sentiment = pd.DataFrame(data)
#     df_positive = df_sentiment[df_sentiment['label'] == 'POSITIVE']
#     df_negative = df_sentiment[df_sentiment['label'] == 'NEGATIVE']
#     return [df_positive['author_id'].nunique(), df_negative['author_id'].nunique()]


@app.callback(Output('trend_graph', 'figure'),  [Input("my_interval", "n_intervals")], prevent_initial_call=False)
def trend_graph(n):
    trends = services_client.get_subreddit_trends()
    return get_trend_graph(pd.DataFrame(trends).sort_values(by='subscribers', ascending=False))





@app.callback(Output('sentiment_graph', 'figure'),  [Input("my_interval", "n_intervals"), ], prevent_initial_call=False)
def make_sentiment_graph(n):
    sentiment_count = get_label_count()
    return get_sentiment_graph(sentiment_count)


@app.callback(Output('emotion_graph', 'figure'),  [Input("my_interval", "n_intervals"), ], prevent_initial_call=False)
def make_emotion_graph(n):
    emotion_count = get_label_count()
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


@app.callback(
    Output('keywords-wordcloud', 'src'),
    [Input('my_interval', 'n_intervals')],
)
def generate_key_wordcloud(n, ):
    text = redis_client.get_data(settings.KAFKA_KEYWORDS_TOPIC)['output'].str.cat()
    if not text:
        dash.exceptions.PreventUpdate
    redis_client.delete_data(settings.KAFKA_KEYWORDS_TOPIC)
    return services_client.get_wordcloud_from_text(text)

@app.callback(
    Output('ner-wordcloud', 'src'),
    [Input('my_interval', 'n_intervals')],
)
def generate_ner_wordcloud(n, ):
    text = redis_client.get_data(settings.KAFKA_NER_TOPIC)['output'].str.cat()
    if not text:
        dash.exceptions.PreventUpdate
    redis_client.delete_data(settings.KAFKA_NER_TOPIC)
    return services_client.get_wordcloud_from_text(text)


if __name__ == '__main__':
    app.run_server(debug=True, port='7020', host='0.0.0.0', dev_tools_prune_errors=True)
