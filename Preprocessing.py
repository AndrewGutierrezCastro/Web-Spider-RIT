import re  # Para la coincidencia de expresiones (regex)
import json # Para manejo de la estructra Json
from sqlite3 import SQLITE_CREATE_TEMP_VIEW

from sqlalchemy import false  # Recipiente de archivos
import RegexPatterns  # Para poder manejar las expresiones del regex
import pandas as pd  # Para poder manipular los datos de codigo
import collections # Para poder manejar listas grandes
from word2number import w2n # Para poder guardar strings a enteros.
from os.path import exists # Para verificar si un archivo existe
from invertedIndex import invertIndex
from Calculo import calc_peso


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


def makeInvertedIndex():
    global documents
    invertedIndex, documents = invertIndex(hashmapData)
    fileContent = json.dumps(invertedIndex, sort_keys=True, indent=4)
    saveFile("invertedIndex.json", fileContent)
    print(invertedIndex.keys(), [len(i) for i in invertedIndex.values()])

# Is used to save file on the file system
def saveFile(fileName, fileContent, mode='w'):
    file = open(fileName, mode)
    file.write(fileContent)
    file.close()

# Is used to calculate the performance of the index and to save it on the file system
def calc_performance(input_file_path,save_file_path = "calc_performance",verbose = false,override = false):
    if override:
        print("Override activated, remaking Performance Calculations!")
    if exists(save_file_path) and not(override):
        print("File "+save_file_path+" exist calc_performance skipped!")
        return
    with open(input_file_path, 'r') as j:
        contents = json.load(j)
    temps = {}
    for key in contents:
        value = contents[key]
        repeated_elements = [item for item, count in collections.Counter(value).items() if count > 1]
        numbered_list = collections.Counter(value).items()
        amount_repeated_list = {}
        #for repeated_elemnt in repeated_elements:
        #    amount_repeated_list[repeated_elemnt] = numbered_list[repeated_elemnt]
        #print(amount_repeated_list)
        temps[key] = numbered_list
    #Se empieza a etirar sobre el indice
    byte_content = []
    verbose_content = ""
    for temp in temps:
        for temp2 in temps[temp]:
            frequency = temp2[1]
            maxi = len(temp2)
            list_documents = documents
            list_documents_found = temps[temp]
            k = 0 # Por default 0, no tiene relevancia si no se utiliza TF: K
            #Tipo_IDF: unaria,suavizada,maxima,probabilistica,inversa
            #Tipo_TF: binario, logaritmica, doble, k, frecuencia
            type_idf = "inversa"
            type_tf = "logaritmica"
            peso = calc_peso(type_idf,type_tf,frequency,k,maxi,list_documents,list_documents_found)
            byte_tag = bytes(temp, 'utf-8')
            byte_doc_id = bytes(temp2[0])
            byte_peso = bytes(peso)
            byte_frequency = bytes(frequency)
            byte_maxi = bytes(maxi)
            byte_k = bytes(k)
            byte_len_docs = bytes(len(list_documents))
            byte_len_found_docs = bytes(len(list_documents_found))
            buffer_bytes = [byte_tag,byte_doc_id,byte_peso,byte_frequency,byte_maxi,byte_k, byte_len_docs, byte_len_found_docs]
            byte_content.extend(buffer_bytes)
            verbose = "Tag: "+temp+" Doc_id: "+str(temp2[0])+" Peso: "+str(peso)+" Freq: "+str(frequency)+" Maxi: "+str(maxi) + " Doc: "+str(len(list_documents))+" Doc_Found: "+str(len(list_documents_found))+"\n"
            verbose_content = verbose_content + verbose
    fileByteArray = b"".join(byte_content)
    print("Saved " + str(len(byte_content))+ " Bytes on "+save_file_path)
    saveFile(save_file_path,fileByteArray,"wb")
    if verbose:
        saveFile(save_file_path+"_verbose.txt",verbose_content)
        print("Saved Verbose File")
    return


def main():
    print("Preprocessing version 0.1 running....")
    load_info()
    preprocessing()
    jsonFile = json.dumps(hashmapData, sort_keys=True, indent=4)
    saveFile("result.json", jsonFile, "w")
    print(str(totalMatches) + " total matches!!!. The JSON file was writed!!")
    makeInvertedIndex()
    calc_performance("invertedIndex.json","calc_performance",True,True)
if __name__ == '__main__':
    main()
