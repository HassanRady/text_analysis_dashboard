from io import BytesIO
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
from redis_handler import RedisClient
import dash_bootstrap_components as dbc
from utils import *
from utils import get_wordcloud

redis_client = RedisClient()

app = dash.Dash(__name__)

refresh_rate_value = 5
MILLISECOND_IN_SECOND = 1000


hidden_div = html.Div(id='placeholder', style={'display': 'none'})

interval = dcc.Interval(
    id='my_interval',
    disabled=False,
    interval=MILLISECOND_IN_SECOND*refresh_rate_value,
    n_intervals=0,
    max_intervals=-1,
)

# # Define the layout
# app.layout = html.Div([interval, hidden_div,
#                         dbc.CardHeader(
#         "Keywords", className="card-header", style={'position': 'center', 'color': '#8898aa'}),

#                        dbc.CardBody([
#                            html.Div(
#                                dbc.CardImg(id='keywords-wordcloud',), className="",
#                            )
#                        ], className=""),

#                        dbc.Card([
#     dbc.CardHeader(
#         "Entities", className="card-header", style={'position': 'center', 'color': '#8898aa'}),

#     dbc.CardBody([
#         # html.Div(
#             dbc.CardImg(id='ner-wordcloud',),
#         # )
#     ], className=""),
# ],
#     className="card shadow",)
#                        ])
# @app.callback(Output('my_interval', 'interval'), Input('refresh_rate', 'value'))
# def set_interval(v):
#     return float(v)*MILLISECOND_IN_SECOND


card_keywords_word_cloud = dbc.Card([
    dbc.CardHeader(
        "Keywords", className="card-header", style={'position': 'center', 'color': '#8898aa'}),

    dbc.CardBody([
        html.Div(
            dbc.CardImg(id='keywords-wordcloud',), className="",
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

app.layout = html.Div([interval,
     dbc.Row([
         dbc.Col(card_keywords_word_cloud, ),
         dbc.Col(card_ner_word_cloud, ),

     ],),])



@app.callback(
    Output('keywords-wordcloud', 'src'),
    # Output('placeholder', 'children'),
    [Input('my_interval', 'n_intervals')],
)
def generate_key_wordcloud(n, ):
    text = redis_client.get_stream_data("keywords_subreddit")['text'].str.cat()
    redis_client.delete_stream_data("keywords_subreddit")

    return get_wordcloud(text)

    # wordcloud = WordCloud(width=800, height=400,
    #                       background_color='white').generate(text)

    # img = BytesIO()
    # wordcloud.to_image().save(img, format='PNG')
    
    # del wordcloud
    # del text
    # return None
    # # return f"data:image/png;base64, {base64.b64encode(img.getvalue()).decode()}"


@app.callback(
    Output('ner-wordcloud', 'src'),
    [Input('my_interval', 'n_intervals')],
)
def generate_ner_wordcloud(n, ):
    text = redis_client.get_stream_data("ner_subreddit")['text'].str.cat()
    redis_client.delete_stream_data("ner_subreddit")

    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(text)
    
    img2 = BytesIO()
    wordcloud.to_image().save(img2, format='PNG')
    del wordcloud
    # del text
    return f"data:image/png;base64, {base64.b64encode(img2.getvalue()).decode()}"


if __name__ == '__main__':
    app.run_server(debug=True, port='7020', host='0.0.0.0', dev_tools_prune_errors=True)
