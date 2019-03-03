# -*- coding: utf-8 -*-
"""
@author: Shivani Tayal
"""

from html.parser import HTMLParser



class MLStripper(HTMLParser):
    """
    This class is used to strip all
    html tags from the raw data.
    """
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

