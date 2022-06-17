import re  # Para la coincidencia de expresiones (regex)
import json # Para manejo de la estructra Json
from sqlite3 import SQLITE_CREATE_TEMP_VIEW
import base64 #Para encodificar a binario

from sqlalchemy import false  # Recipiente de archivos
import RegexPatterns  # Para poder manejar las expresiones del regex
import pandas as pd  # Para poder manipular los datos de codigo
import collections # Para poder manejar listas grandes
from word2number import w2n # Para poder guardar strings a enteros.
from os.path import exists,getsize # Para verificar si un archivo existe y Obtener el tamaño de un archivo.
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
documents = []
documentsFullData = []
# Con ayuda del regex, lo que hace es filtar de una manera mas limpia la informacion de los
# distintos componentes. Configurada cada una de ellas en el archivo de RegexPatterns

'''
    Funcion para aplicar elementos de regEx a un string.
    stringWords: Una lista de palabras para aplicar el regEx
    regexPattern: Una lista con los patrones de RegEx
    Args: stringWords(Str),regexPattern(Str)
    Return: String
'''
def denoise_text(stringWords, regexPattern):
    return re.findall(regexPattern, stringWords, re.IGNORECASE)
# Carga la info de cada componente en el hashmap

'''
    Funcion para cargar toda la informacion necesaria a memoria.
    Args: None
    Return: None
'''
def load_info():
    global hashmapData, documentsFullData
    index = 0
    for name in FILENAME.keys():
        data = pd.read_csv(name + FILETYPE)
        hashmapData[name] = data
        columns = ["index"] + data.columns.to_list()
        for document in data.itertuples():
            document = list(document) 
            document = dict(zip(columns, [ index + 1 ] + document[1:5]))
            documentsFullData.append(document)
            index += 1
# Ya estando los archivos cargados en el hashmap, se encarga de
# aplicar la funcion del denoise_text

'''
    Funcion para eliminar varios elementos basura de nuestro modelo.
    Args: None
    Return: None
'''
def preprocessing():
    global hashmapData
    for name in hashmapData.keys():
        data = hashmapData[name]
        descriptionList = data.Desc_Producto.tolist()
        result = []
        for i in descriptionList:
            result.append(denoise_text(i, FILENAME[name]))
        hashmapData[name] = result

'''
    Funcion para crear un indice invertido y lo guarda en un formato json.
    Args: None
    Return: None
'''
def makeInvertedIndex():
    global documents
    invertedIndex, documents = invertIndex(hashmapData)
    jsonFile = json.dumps(documents, sort_keys=True, indent=4)
    saveFile("documents.json", jsonFile, "w")
    jsonFile = json.dumps(documentsFullData, sort_keys=True, indent=4)
    saveFile("documentsFullData.json", jsonFile, "w")
    fileContent = json.dumps(invertedIndex, sort_keys=True, indent=4)
    saveFile("invertedIndex.json", fileContent)

'''
    Funcion para escritura de contenido en archivos.
    fileContent: Variable que guarda el contenido que se quiere escribir.
    fileName: Variable que guarda la locacion donde se quiere guardar el archivo.
    mode: Variagle que guarda el tipo de escritura que se requiere.
    Args:fileName(Str), fileContent(Str),mode(Str)
    Return: None
'''
def saveFile(fileName, fileContent, mode='w'):
    file = open(fileName, mode)
    file.write(fileContent)
    file.close()

'''
    Funcion para el Calculo de pesos de los terminos en los archivos.
    input_file_path: Variable que guarda la locacion donde se encuentra el indice del vocabulario.
    save_file_path: Variable que guarda la locacion donde se quiere guardar el archivo binario
    verbose: Variable para verificar si la funcion ocupa crear un archivo .json
    override: Variable para verificar si la funcion omite el archivo ya guardado.
    Args:input_file_path(Str), save_file_path(Str),verbose(Bool),override(Bool)
    Return: JsonObject
'''
def calc_pesos(input_file_path,save_file_path = "calc_pesos",verbose = false,override = false):
    if override:
        print("Override activated, remaking Vector Weight Calculations!")
    if exists(save_file_path) and not(override):
        print("File "+save_file_path+" exist calc_pesos skipped!")
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
    verbose_content_total = {"total_index":[]}
    for temp in temps:
        verbose_content = {"tag": temp, "matches":[]}
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
            verbose = {
                "doc_id": temp2[0], 
                "peso":peso, 
                "freq":frequency, 
                "maxi":maxi, 
                "cant_doc":len(list_documents),
                "cant_doc_found":len(list_documents_found)
                }
            verbose_content["matches"].append(verbose)
        verbose_content_total["total_index"].append(verbose_content)
    jsondump = json.dumps(verbose_content_total, indent=4)
    #saveFile(save_file_path,verbose_content_total,"wb")
    bin_json = base64.b64decode(jsondump + str(b'=='))
    saveFile(save_file_path,bin_json,"wb")
    file_size = getsize(save_file_path)
    print("Saved " + str(file_size)+ " Bytes on "+save_file_path)
    if verbose:
        saveFile(save_file_path+"_verbose.json",jsondump)
        print("Saved Verbose File size: "+str(getsize(save_file_path+"_verbose.json"))+" Bytes")
    return


def main():
    print("Preprocessing version 0.1 running....")
    load_info()
    preprocessing()
    jsonFile = json.dumps(hashmapData, sort_keys=True, indent=4)
    saveFile("result.json", jsonFile, "w")
    print("The JSON file was writed!!")
    makeInvertedIndex()
    calc_pesos("invertedIndex.json","calc_pesos",True,True)
if __name__ == '__main__':
    main()
