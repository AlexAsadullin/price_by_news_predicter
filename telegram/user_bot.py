import telebot  # для работы с ботом
from telebot import types  # для создания кнопок
import asyncio
import json
from tg_news_parser import *

TOKEN = '6264223116:AAGePEZ4nxkmPgabXHi6NeeT0rXkqGIzvWQ'
bot = telebot.TeleBot(TOKEN)
MESSG = {}
USER = {}
QUERY = {}


@bot.message_handler(commands=['start'])
def hello(message):  # hello функция
    welcome_message = f"""Hi, {message.chat.username}!\nI'm _name_ bot\nI will help you to get news from finance world."""
    MESSG['chat_id'] = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    bt1 = types.KeyboardButton('Get news')
    bt2 = types.KeyboardButton('My profile')
    markup.add(bt1, bt2)
    bt1 = types.InlineKeyboardButton('Set new auto parsing')
    bt2 = types.InlineKeyboardButton('My auto parsers')
    markup.add(bt1, bt2)
    bt1 = types.InlineKeyboardButton('New price monitoring')
    bt2 = types.InlineKeyboardButton('My price monitors')
    markup.add(bt1, bt2)
    bot.send_message(message.chat.id, welcome_message,
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def callback_message1lv(message):
    global MESSG
    if message.text == 'Get news':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Tg channel'))
        markup.add(types.KeyboardButton('Web page'))
        bot.send_message(message.chat.id, 'what is your source?', reply_markup=markup)
    elif message.text == 'Set new auto parsing':
        bot.send_message(message.chat.id, text='auto parsing')

    if message.text == 'Tg channel':
        ## func from news_parser
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, text='Type tg channel id\nYou can get it here @getmyid_bot')
        bot.register_next_step_handler(msg, get_channel_id)  # вызываем функцию для считывания срока


def get_channel_id(message):
    channel_id = int(message.text)
    QUERY['channel_id'] = channel_id
    msg = bot.send_message(message.chat.id, text='Type keywords for search (sep by space) like:\nтинькофф сбер втб')
    bot.register_next_step_handler(msg, get_keywords)  # вызываем функцию для считывания срока


def get_keywords(message):
    keywords = message.text.split()
    QUERY['keywords'] = keywords
    msg = bot.send_message(message.chat.id, text='Type number of days you will be looking back')
    bot.register_next_step_handler(msg, get_lookback)  # вызываем функцию для считывания срока


def get_lookback(message):
    lookback = int(message.text)
    QUERY['lookback'] = lookback
    history = asyncio.run(read_tg_channel(channel_id=QUERY['channel_id'],
                                          keywords=QUERY['keywords'],
                                          lookback=QUERY['lookback']))
    bot.send_message(message.chat.id, text='request has been created successfully, please wait')
    file = json.dumps(history)
    bot.send_document(message.chat.id, file)


bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()

bot.infinity_polling()
