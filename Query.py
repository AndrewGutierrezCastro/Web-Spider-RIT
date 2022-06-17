import json
import numpy as np
import pandas
from vectors import getVectorsFromFile
from vectors import getVectorsFromKeys
from Calculo import calc_sim

def openFile(name):
    f = open(name,'r',encoding='utf-8')
    data = json.loads(f.read())
    f.close()
    return data

def getDocs(query):
    data = openFile("calc_pesos_verbose.json")
    documents = []
    total_index = data["total_index"]
    for term in query:
        for dictionary in total_index:
            if dictionary["tag"] == term.lower():
                matches = dictionary["matches"]
                documents += matches
    return documents


def getDocsSortedByWeight(queryStr):
    queryLst = queryStr.split(",")
    documents = getDocs(queryLst)
    df = pandas.DataFrame(documents)
    df = df.sort_values(by='peso', ascending=False)
    return df.head(n=20)

def calculo_similitud(vector1, vector2):
    similitud = []
    for v in vector1:
        similitud.append(calc_sim(v,vector2))
    return similitud

def getDocsWithAllData(docs_Ids : list):
    data = openFile("documentsFullData.json")
    documents = {}
    docs_finded = []
    for doc in data:
        if doc["index"] in docs_Ids and doc["index"] not in docs_finded :
            docs_finded.append(doc["index"])
            documents[doc["index"]] = doc
    result = []
    for id in docs_Ids:
        result.append(documents[id])
    return result


def query(queryStr):
    vectorsCollection = getVectorsFromFile("calc_pesos_verbose.json")
    queryResult = getDocsSortedByWeight(queryStr)
    queryWeightVector = queryResult["peso"].tolist()
    queryDocumentIdList = queryResult["doc_id"].tolist()
    v = getVectorsFromKeys(vectorsCollection,queryDocumentIdList)
    similitud = calculo_similitud(v,queryWeightVector)
    queryResult["similitud"] = similitud
    queryResult = queryResult.sort_values(by='similitud', ascending=False)
    documentsFullData = getDocsWithAllData(list(queryResult["doc_id"]))
    return documentsFullData, queryResult

query("atx,8gb,mid-tower,tempered glass")