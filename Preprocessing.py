import re
import RegexPatterns
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize

FILENAME = ["CASE","CPU","GPU","HDD","MotherBoard","PSU","RAM","SSD"]
FILETYPE = ".csv"

hashmapData = {}

def tokenizer(string):
    return word_tokenize(string)

def denoise_text(stringWords, regexPattern):
    return re.findall(regexPattern, stringWords, re.IGNORECASE)

def load_info():
    global hashmapData
    for name in FILENAME:
        data = pd.read_csv(name + FILETYPE)
        hashmapData[name] = data
    

def preprocessing():
    global hashmapData
    #load_info() TODO check fields and content on csv files missmatching 
    # pandas.errors.ParserError: Error tokenizing data. C error: Expected 4 fields in line 529, saw 5
    #TODO denoise_text for each file
    data = pd.read_csv("GPU.csv")
    descriptionList = data.Desc_Producto.tolist()
    #print(descriptionList[:5])
    for i in descriptionList:
        
        result = denoise_text(i, RegexPatterns.GPUPATTERN)
        print(result)

if __name__ == '__main__':
    print("Preprocessing version 0.1 running....")
    preprocessing()