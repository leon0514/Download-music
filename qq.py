    
'''qq.py'''
import requests
import json

def qqgetsongs(keyword):
    if keyword is None:
        return
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        'Content-Length': '0',
    }
    data = []
    response = requests.get('https://api.bzqll.com/music/tencent/search?key=579621905&s={}&limit=100&offset=0&type=song'.format(keyword),headers=headers)
    songs = json.loads(response.text)
    for song in songs['data']:
        data.append([song['name'],song['url'],song['singer']])
    return data
