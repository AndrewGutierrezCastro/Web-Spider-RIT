import re
import json

from attr import has
import RegexPatterns
import pandas as pd

FILENAME = {"CASE":RegexPatterns.CASEPATTERN,
            "CPU":RegexPatterns.CPUPATTERN,
            "GPU":RegexPatterns.GPUPATTERN,
            "HDD":RegexPatterns.HDDPATTERN,
            "MotherBoard":RegexPatterns.MOTHERBOARDPATTERN,
            "PSU":RegexPatterns.PSUPATTERN,
            "RAM":RegexPatterns.RAMPATTERN,
            "SSD":RegexPatterns.SSDPATTERN}
FILETYPE = ".csv"

hashmapData = {}

def denoise_text(stringWords, regexPattern):
    return re.findall(regexPattern, stringWords, re.IGNORECASE)

def load_info():
    global hashmapData
    for name in FILENAME.keys():
        data = pd.read_csv(name + FILETYPE)
        hashmapData[name] = data
    

def preprocessing():
    global hashmapData
    for name in hashmapData.keys():
        data = hashmapData[name]
        descriptionList = data.Desc_Producto.tolist()
        for i in descriptionList:
            result = denoise_text(i, FILENAME[name])
            print(result)

if __name__ == '__main__':
    print("Preprocessing version 0.1 running....")
    load_info()
    preprocessing()
    print(json.dumps(hashmapData, sort_keys=True, indent=4))