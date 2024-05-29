import telebot  # для работы с ботом
from telebot import types  # для создания кнопок
import asyncio
import json
from tg_news_parser import *

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
MESSG = {}
USER = {}
QUERY = {}


@bot.message_handler(commands=['start'])
def hello(message):  # hello функция
    welcome_message = f"""Hi, {message.chat.username}!\n I'm your manager of ai news classificator\nWhich ai you want to pick"""
    MESSG['chat_id'] = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    bt1 = types.KeyboardButton('')
    bt2 = types.KeyboardButton('')
    markup.add(bt1, bt2)
    bt1 = types.KeyboardButton('')
    bt2 = types.KeyboardButton('')
    markup.add(bt1, bt2)
    bt1 = types.KeyboardButton('')
    bt2 = types.KeyboardButton('')
    markup.add(bt1, bt2)
    bot.send_message(message.chat.id, welcome_message,
                     reply_markup=markup)


