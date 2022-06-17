import json
import numpy as np
import pandas
from vectors import getVectorsFromFile
from vectors import getVectorsFromKeys
from Calculo import calc_sim

def openFile():
    f = open("calc_pesos_verbose.json",'r',encoding='utf-8')
    data = json.loads(f.read())
    f.close()
    return data

def getDocs(query):
    data = openFile()
    documents = []
    total_index = data["total_index"]
    for term in query:
        for dictionary in total_index:
            if dictionary["tag"] == term.lower():
                matches = dictionary["matches"]
                documents += matches
    return documents


def query(queryStr : str):
    queryLst = queryStr.split(",")
    documents = getDocs(queryLst)
    df = pandas.DataFrame(documents)
    df = df.sort_values(by='peso', ascending=False)
    return df.head(n=20)

def calculo_similitud(vector1, vector2):
    similitud = []
    for v in vector1:
        similitud.append(calc_sim(v,queryWeightVector))
    return similitud

vectorsCollection = getVectorsFromFile("calc_pesos_verbose.json")
queryResult = query("atx,8gb,mid-tower,tempered glass")
queryWeightVector = queryResult["peso"].tolist()
queryDocumentIdList = queryResult["doc_id"].tolist()
v = getVectorsFromKeys(vectorsCollection,queryDocumentIdList)
#print(queryResult)
#print(queryWeightVector[:2])
#print(queryDocumentIdList)
#print(vectorsCollection)
#print(v)
similitud = calculo_similitud(v,queryWeightVector)
print(similitud)
#calc_sim(queryResult["peso"])
