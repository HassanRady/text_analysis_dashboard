import requests

def get_ner(text):
    url = "http://127.0.0.1:9005/ner"
    field = 'text'
    body  = {field: text.tolist()}
    response = requests.post(url=url, json=body)
    return response.json()