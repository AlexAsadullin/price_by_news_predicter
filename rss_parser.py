import json
import requests
import xmltodict
import pandas as pd


def create_dataframe(filename: str):
    rss_ribbon_dict = json.load(open(f'{filename}.json', "rb"))
    news = rss_ribbon_dict['rss']['channel']['item']
    pandas_news = []
    for i in news:
        row = {}
        # keys might be different
        row['title'] = i['title']
        row['category'] = i['category']
        row['date'] = i['rbc_news:date']#['__text']
        row['time'] = i['rbc_news:time']#['__text']
        row['full-text'] = i['rbc_news:full-text']#['__cdata']
        row['tag'] = ''
        try:
            for tag in i['rbc_news:tag']:
                row['tag'] += tag + ' '
            pandas_news.append(row)
        except Exception as e:
            print(e)
    news_df = pd.DataFrame(pandas_news)
    news_df.to_csv('news.csv')


def parse_xml(filename: str):
    file = open(f'{filename}.xml', "rb")
    news_dict = xmltodict.parse(file)

    with open(f'{filename}.json', 'w') as f:
        f.write(json.dumps(news_dict))
    return news_dict


def download_rss_xml(url: str, filename: str):
    response = requests.get(url)
    response.raise_for_status()
    xml_content = response.content

    with open(f"{filename}.xml", "wb") as f:
        f.write(xml_content)
    return xml_content


if __name__ == '__main__':
    rss_url = 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'
    filename = 'news'
    xml_content = download_rss_xml(rss_url, filename)
    news_dict = parse_xml(filename)
    parse_xml(filename)

    create_dataframe(filename)
