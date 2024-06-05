import json

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import seaborn as sns
import re
import os
import sys
import csv
import codecs
import pymorphy2
# import gensim

import nltk
from nltk.stem.snowball import SnowballStemmer  # russian lang
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score  # to install type 'scikit-learn'
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

sys.path.insert(1, os.path.join(sys.path[0], '..'))

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
sns.set_style("darkgrid")

# константы
COMPANY = 'AAPL'  # ticker of stock
PREDICTION_DAYS = 365  # days looking back to


def load_data():
    data = json.loads('data\\rbc')
    print(data)
    # $$$ import data


def preprocess(text):
    stopWords = set(stopwords.words('russian'))

    reg = re.compile('[^а-яА-Яa-zA-Z0-9 ]')  #
    text = text.lower().replace("ё", "е").replace("ъ", "ь").replace("й", "и")
    text = reg.sub(' ', text)
    # Лемматизация + stop words
    morph = pymorphy2.MorphAnalyzer()
    text = [morph.parse(word)[0].normal_form for word in text.split() if word not in stopWords]
    text = ' '.join(text)

    return text


def prepare_data(data):
    x_train, x_test, y_train, y_test = train_test_split()

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
    # возвращаем выборки и модель масштабирования
    return x_train, y_train, scaler


def bow(x_train, x_test):
    vectorizer = CountVectorizer(ngram_range=1, 2)
    x_train_bow = vectorizer.fit_transform(x_train)
    x_test_bow = vectorizer.transform(x_test)


def tfidf(x_train, x_test):
    vectorizer = TfidfVectorizer()
    x_train_tfidf = vectorizer.fit_transform(x_train)
    x_test_tfidf = vectorizer.transform(x_test)


def building_model(x_train_bow, y_train):
    clf = LogisticRegression(random_state=0).fit(x_train_bow, y_train)
    # создаем модель

    # получаем признаки и цели из аргументов

    # инициализируем модель
    model = Sequential()
    # создаем слои нейросети для обучения модели
    model.compile(optimizer='adam', loss='mean_squared_error')
    # обучаем модель
    model.fit(x_train, y_train, epochs=95, batch_size=32)
    # сохраняем модель
    model.save('predicter_v1')
    # возвращаем обученную модель
    return model


if __name__ == '__main__':
    load_data()
