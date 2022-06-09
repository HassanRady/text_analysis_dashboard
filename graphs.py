from functions import *
from plotly import graph_objs as go


def get_sentiment_graph(sentiment_count):
    
    def __get_color(sentiment):
        if sentiment == 'POSITIVE':
            return '#00d1ff'
        elif sentiment == 'NEGATIVE':
            return '#ff4a55'
        else:
            return '#33ffe6'

    data = [go.Pie(
            labels=sentiment_count.index,
            values=sentiment_count,
            marker=dict(
                colors=[__get_color(sentiment)
                        for sentiment in sentiment_count.index],
            ),
            text=[l for l in sentiment_count.index],
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


