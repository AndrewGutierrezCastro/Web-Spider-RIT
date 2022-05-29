import re  # Para la coincidencia de expresiones (regex)
import json  # Recipiente de archivos
import RegexPatterns  # Para poder manejar las expresiones del regex
import pandas as pd  # Para poder manipular los datos de codigo

from invertedIndex import invertIndex

FILENAME = {"CASE": RegexPatterns.CASEPATTERN,
            "CPU": RegexPatterns.CPUPATTERN,
            "GPU": RegexPatterns.GPUPATTERN,
            "HDD": RegexPatterns.HDDPATTERN,
            "MotherBoard": RegexPatterns.MOTHERBOARDPATTERN,
            "PSU": RegexPatterns.PSUPATTERN,
            "RAM": RegexPatterns.RAMPATTERN,
            "SSD": RegexPatterns.SSDPATTERN}
FILETYPE = ".csv"

hashmapData = {}
totalMatches = 0
documents = []
# Con ayuda del regex, lo que hace es filtar de una manera mas limpia la informacion de los
# distintos componentes. Configurada cada una de ellas en el archivo de RegexPatterns


def denoise_text(stringWords, regexPattern):
    return re.findall(regexPattern, stringWords, re.IGNORECASE)
# Carga la info de cada componente en el hashmap


def load_info():
    global hashmapData
    for name in FILENAME.keys():
        data = pd.read_csv(name + FILETYPE)
        hashmapData[name] = data

# Ya estando los archivos cargados en el hashmap, se encarga de
# aplicar la funcion del denoise_text


def preprocessing():
    global hashmapData, totalMatches
    for name in hashmapData.keys():
        data = hashmapData[name]
        descriptionList = data.Desc_Producto.tolist()
        result = []
        for i in descriptionList:
            result.append(denoise_text(i, FILENAME[name]))
        totalMatches += len(result)
        hashmapData[name] = result


def makeInvertedIndex(query=["ATX", "Mid-Tower"]):
    global documents
    invertedIndex, documents = invertIndex(hashmapData, query)
    fileContent = json.dumps(invertedIndex, sort_keys=True, indent=4)
    saveFile("invertedIndex.json", fileContent)
    print(invertedIndex.keys(), [len(i) for i in invertedIndex.values()])


def saveFile(fileName, fileContent, mode='w'):
    file = open(fileName, mode)
    file.write(fileContent)
    file.close()


def main():
    print("Preprocessing version 0.1 running....")
    load_info()
    preprocessing()
    jsonFile = json.dumps(hashmapData, sort_keys=True, indent=4)
    saveFile("result.json", jsonFile, "w")
    print(str(totalMatches) + " total matches!!!. The JSON file was writed!!")
    makeInvertedIndex(["ATX", "Mid-tower", "CPU", "8GB", "DDR4"])


if __name__ == '__main__':
    main()
