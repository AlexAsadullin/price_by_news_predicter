import json
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et

import pandas as pd
import ssl
import time as t
from load_stock_data import save_data

def load_xml(url: str):
    r = requests.get(url)
    r.raise_for_status()
    with open('rbc.xml', "w", encoding='utf8') as file:
        file.write(r.text)
    '''
    file = et.parse(r.text)
    print(file)
    for type_tag in file.findall('shop/offers/offer'):
        value = type_tag.find('name').text
        print(value)
    '''

def load(url: str, features: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features=features)
    article = soup.find()
    data = article.text.split('\n')
    return data


def cleaning(data: list, params: list):
    new_data = []
    for news in data:
        for parameter in params:
            if parameter in news:
                break
        else:
            new_data.append(news)
    return new_data


data = load_xml(url='http://static.feed.rbc.ru/rbc/logical/footer/news.rss')
# save_data(name='rbc', data=data, extension='json')
