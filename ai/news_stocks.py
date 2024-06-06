import joblib
import pandas as pd
import seaborn as sns
import re
import os
import sys

import pymorphy3
# import gensim

import nltk
from nltk.stem.snowball import SnowballStemmer  # russian lang
from nltk.stem import WordNetLemmatizer

# to install type 'scikit-learn'
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from tensorflow.keras import Sequential

nltk.download('stopwords')
'''os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
sns.set_style("darkgrid")'''


def load_data_csv(name: str):
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(f'{name}.csv')))
    news_df = pd.read_csv(f'{parent_dir}/{name}.csv')

    return news_df  # pandas dataframe


def format_text(text):
    from nltk.corpus import stopwords
    stopWords = set(stopwords.words('russian'))

    reg = re.compile('[^а-яА-Яa-zA-Z0-9 ]')  #
    text = text.lower().replace("ё", "е").replace("ъ", "ь").replace("й", "и").replace("&laquo;", '').replace("&raquo;",
                                                                                                             '').replace(
        "&nbsp;", '').replace("&mdash;", '')
    text = reg.sub(' ', text)
    # Лемматизация + stop words
    morph = pymorphy3.MorphAnalyzer()
    text = [morph.parse(word)[0].normal_form for word in text.split() if word not in stopWords]
    text = ' '.join(text)

    return text  # is 1 string


def text_train_split(df):
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(df['formatted-text'], df['growth'], test_size=.15,
                                                        random_state=42)
    return x_train, x_test, y_train, y_test  # strings


def bow(x_train, x_test):
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    x_train_bow = vectorizer.fit_transform(x_train)
    x_test_bow = vectorizer.transform(x_test)

    return x_train_bow, x_test_bow  # lists of digits


def building_model(x_train_bow, y_train):
    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression(random_state=0).fit(x_train_bow, y_train)
    joblib.dump(clf, "model.pkl")
    return clf


def test_model(clf, x_train_bow, y_test):
    from sklearn.metrics import accuracy_score
    y_predict = clf.predict(x_train_bow)
    print(x_train_bow, y_test, y_predict)
    return accuracy_score(y_predict, y_test)


if __name__ == '__main__':
    news_df = load_data_csv('news')
    news_df['formatted-text'] = news_df['full-text'].apply(format_text)
    # creating as;dfkjasd;fkj
    x_train, x_test, y_train, y_test = text_train_split(news_df)
    x_train_bow, x_test_bow = bow(x_train, x_test)

    classificator = building_model(x_train_bow, y_train)
    # print(test_model(classificator, x_train_bow, y_test))

    news_df.to_csv('news_to_learn.csv')
