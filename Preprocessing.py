import re
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize

FILENAME = ["CASE","CPU","GPU","HDD","MotherBoard","PSU","RAM","SSD"]
FILETYPE = ".csv"

hashmapData = {}

def tokenizer(string):
    return word_tokenize(string)

def denoise_text(stringWords, regexPattern):
    return re.findall(regexPattern, stringWords)

def load_info():
    global hashmapData
    for name in FILENAME:
        data = pd.read_csv(name + FILETYPE)
        hashmapData[name] = data
    

def preprocessing():
    global hashmapData
    #TODO denoise_text for each file
    

if __name__ == '__main__':
    print("Preprocessing version 0.1 running....")
    preprocessing()