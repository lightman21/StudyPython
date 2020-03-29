import inspect
import os
import sys


import html


class KCEBean:
    def __init__(self, key, cn, en):
        self.key = key
        self.cn = cn
        self.en = en

    def __str__(self):
        return "key: " + str(self.key) + "\tcn: " + str(self.cn) + "\ten: " + str(self.en)


    def __lt__(self, other):
        return self.key.lower() < other.key.lower()


class XmlStdin:
    def __init__(self):
        self.str = ""

    def write(self, value):
        self.str += value

    def toString(self):
        txt = html.unescape(self.str)
        return txt
