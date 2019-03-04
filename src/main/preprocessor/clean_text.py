# -*- coding: utf-8 -*-
"""
@author: Shivani Tayal
"""

from html.parser import HTMLParser
import unicodedata
import sys
from nltk.corpus import stopwords
import codecs
import config


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def cleantext(dataframe):
    dataframe = dataframe.replace({'\n': '',
                                   '-': '',
                                   '"': '',
                                   r'\\\\': '',
                                   r'\.': '', r"\'": "", r'\|': '', r'\।': '', '/': '', r'\(': '', r'\)': '', r'\,': '',
                                   '\’': "", r"\:": ""}, regex=True)
    return dataframe


tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))

def remove_punctuation(text):
    return text.translate(tbl)


class Tokenizer():

    def __init__(self, lang=None, path=None):
        if lang is None:
            self.lang = "gu"
        else:
            self.lang = lang
        if path is None:
            self.path = config.filepath.stopword_path
        else:
            self.path = path
        self.stopwords = set(line.strip() for line in codecs.open(self.path))

    def getstopwords(self):
        stopwords_path = self.path
        print(stopwords_path)
        stopset = set(line.strip() for line in codecs.open(stopwords_path))
        #stopset = self.stopwords
        stopset.update(['.', ',', '"', "'", '?', '!', '>', ':', ';', '(', ')', '[', ']', '{', '}', '।', '/'])
        stopset.update(set(stopwords.words('english')))
        return stopset

    # Takes textfile Splits on
    def gu_tokenize(self, text):
        stopwords = self.getstopwords()
        # print(stopwords)
        sentence = text.split(".")
        # sentence = re.split("[, ]+",sentence)
        sentences_list = sentence
        tokens = []
        for each in sentences_list:
            word_l = each.replace("\r\n", " ").split(" ")
            word_list = [i for i in word_l if not i == '']
            tokens += [i.strip() for i in word_list if i.lower() not in stopwords if not i.isdigit() and len(i) > 5]
        return tokens

    def hi_tokenizer(self, text):
        print("Implement this function")
        pass

    def en_tokenizer(self, text):
        print("Implement this function")
        pass

    def tokenizer(self, text):
        if self.lang == "gu":
            self.gu_tokenize(text)
        elif self.lang == "hi":
            self.hi_tokenizer(text)
        elif self.lang == "en":
            self.en_tokenizer(text)

tok = Tokenizer()

tok.tokenizer("LIfe is good")