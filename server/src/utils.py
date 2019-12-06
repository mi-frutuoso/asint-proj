import hashlib

class Storage:
    def __init__ (self):
        self.data = {}
    def getSize(self):
        return len(self.data)
    def store(self, val):
        try:
            #self.id = hashlib.sha1(str.encode(val)).hexdigest() TODO secretariat id
            self.data[val] +=1
        except:
            self.data[val] = 1
    def getKeys(self):
        return self.data.keys()
    def getValue(self, key):
        try:
            return self.data[key]
        except:
            return None

import sys
import pickle

class book:
    def __init__(self, author, title, year):
        self.author = author
        self.title = title
        self.year = year
        self.id = hashlib.sha1(str.encode(year+author+title)).hexdigest()
        print('[created book w/ id = '+self.id+']')