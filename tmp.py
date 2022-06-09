
# table_header = [
#     html.Thead(
#         html.Tr([
#             html.Th("Tweet"),
#             html.Th("Name"),
#             html.Th("Screen Name"),
#             html.Th("Location"),
#             html.Th("Topic"),
#         ]),
#         className="thead-light"), ]

# table_body = [
#     html.Tbody(

#         [html.Tr([html.Td(row['text'], style={'whiteSpace': 'normal',
#                                               'height': 'auto',
#                                               'width': 'auto',
#                                               'word-wrap': 'break-word'}), html.Td(row['name'], style={'whiteSpace': 'normal',
#                                                                                                        'height': '100px',
#                                                                                                        'width': '50px',
#                                                                                                        'word-wrap': 'break-word'}), html.Td(row['screen_name'], style={'whiteSpace': 'normal',
#                                                                                                                                                                        'height': 'auto',
#                                                                                                                                                                        'width': 'auto',
#                                                                                                                                                                        'word-wrap': 'break-word'}),
#                   html.Td(row['location'], style={'whiteSpace': 'normal',
#                                                   'height': 'auto',
#                                                   'width': 'auto',
#                                                   'word-wrap': 'break-word'}), html.Td(row['topic'], style={'whiteSpace': 'normal',
#                                                                                                             'height': 'auto',
#                                                                                                             'width': 'auto',
#                                                                                                             'word-wrap': 'break-word'})]) for i, row in df_show.iterrows()], className="",)
# ]

# card_table = dbc.Card(
#     [
#         dbc.CardHeader(html.H2(
#             "Tweets"), class_name="card-header bg-transparent row align-items-center mb-0"),
#         dbc.CardBody([
#             html.Div([
#                 dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True, striped=False,  style={},
#                           class_name="table ",),
#             ], className="table-responsive"),
#         ],
#             className="table-responsive"),
#     ],
#     class_name="card shadow",

# )