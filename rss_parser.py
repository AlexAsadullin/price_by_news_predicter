import json
import requests
import xml.etree.ElementTree as ET


from load_stock_data import save_data


def cleaning(data: list, params: list):
    new_data = []
    for news in data:
        for parameter in params:
            if parameter in news:
                break
        else:
            new_data.append(news)
    return new_data


def load_xml(url: str):
    pass


def parse_xml():
    way = r''
    tree = ET.parse(way)
    root = tree.getroot()
    root.find('')

url = 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'
r = requests.get(url)



print(dir(r))
print(r.text)
# save_data(name='rbc', data=data, extension='json')
