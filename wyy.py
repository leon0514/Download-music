'''wyy.py'''
import requests
import json

def wygetsongs(keyword):
    if keyword is None:
        return
    data = []

    response = requests.get('https://api.mlwei.com/music/api/wy/?key=523077333&id={}&type=so&cache=0&nu=100'.format(keyword))
    songs = json.loads(response.text)
    for d in songs['Body']:
        data.append([d['title'],d['url'],d['author']])
    return data
    
