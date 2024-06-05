import asyncio
import re
import datetime as dt
import pyrogram
import telebot
import subprocess
from collections import defaultdict
from load_stock_data import save_data

# tg bot config data
api_id = 27652585
api_hash = '7484bada002fc45758ce353a31ff2da1'
history = defaultdict(list)


def remove_emoji(data):
    regrex_pattern = re.compile(pattern="["
                                        u"\U00000000-\U00000009"
                                        u"\U0000000B-\U0000001F"
                                        u"\U00000080-\U00000400"
                                        u"\U00000402-\U0000040F"
                                        u"\U00000450-\U00000450"
                                        u"\U00000452-\U0010FFFF"
                                        "]+", flags=re.UNICODE)
    cleared_data = []
    for text in data:
        cleared_data.append(regrex_pattern.sub(r'', text))
    return cleared_data


def remove_nulls(data: list | tuple | str):
    cleared_data = []
    for i in data:
        if i is not None:
            cleared_data.append(i)
    return cleared_data


async def read_tg_channel(channel_id: int, lookback=7):
    client = pyrogram.Client(name='client1', api_id=api_id, api_hash=api_hash)
    await client.start()
    try:
        actual_time_unix = dt.datetime.now().timestamp()
        days_back_unix = lookback * 24 * 60 * 60  # convert days to seconds (unix)
        end = actual_time_unix - days_back_unix
        messages = client.get_chat_history(chat_id=channel_id, limit=1000)
        news = []
        async for i in messages:
            if i.date.timestamp() < end:
                break
            news.append(i.text)
        print('info added successfully')
    finally:
        await client.stop()
        return news


data = asyncio.run(read_tg_channel(channel_id=-1001498653424))
data = remove_nulls(data)
data = remove_emoji(data)
save_data(name='tg_rbc_invest', data=data, extension='json')
