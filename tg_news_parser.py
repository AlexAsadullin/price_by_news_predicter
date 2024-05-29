from collections import defaultdict
import re
import datetime as dt
import pyrogram

# tg bot config data
api_id = 27652585
api_hash = '7484bada002fc45758ce353a31ff2da1'


def remove_emoji(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U00000000-\U00000009"
                                        u"\U0000000B-\U0000001F"
                                        u"\U00000080-\U00000400"
                                        u"\U00000402-\U0000040F"
                                        u"\U00000450-\U00000450"
                                        u"\U00000452-\U0010FFFF"
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


async def read_tg_channel(channel_id: int, keywords: list, lookback=7):
    client = pyrogram.Client(name='client1', api_id=api_id, api_hash=api_hash)
    await client.start()
    history = defaultdict(list)
    try:
        actual_time_unix = dt.datetime.now().timestamp()
        days_back_unix = lookback * 24 * 60 * 60  # convert days to seconds (unix)
        end = actual_time_unix - days_back_unix
        messages = client.get_chat_history(chat_id=channel_id, limit=10000)
        async for i in messages:
            if i.date.timestamp() < end:
                break
            for j in keywords:
                if j in i.text:
                    history[i.date.strftime('%Y-%m-%d %H:%M')].append(i.text)
                    break
        print('info added successfully')
    finally:
        await client.stop()
        return history
