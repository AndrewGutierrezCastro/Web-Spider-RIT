import json

import pandas

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


print(query("atx,8gb,mid-tower,tempered glass"))
