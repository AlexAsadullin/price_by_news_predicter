import json
import requests
import xmltodict



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
    xml_content = download_rss_xml(rss_url, 'news')
    news_dict = parse_xml('news')
    parse_xml('news.xml')
