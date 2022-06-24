import requests


async def extract_keywords(text):
    url = "http://127.0.0.1:9004/extract"
    field = 'text'
    body  = {field: text.tolist()}
    response = requests.post(url=url, json=body)
    return response.text