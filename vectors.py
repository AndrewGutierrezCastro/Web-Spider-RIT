import json

def getVectorsFromFile(filepath):
    vectorsDocumentos = {}
    f = open(filepath,'r',encoding='utf-8')
    data = json.loads(f.read())
    f.close()
    #print(data)
    total_index = data["total_index"]
    #filtered = {key:value for data.items() if key == "team_name" and value == "myval" or key == "release_train" and value == "my value"}
    names = []
    #print(vectorsDocumentos.get(17679))
    for dictionary in total_index:
        for dic in dictionary["matches"]:
            peso = []
            id = dic["doc_id"]
            peso.append(dic["peso"])
            if vectorsDocumentos.get(id) == None:
                vectorsDocumentos.update({id:peso})
            else:
                peso = vectorsDocumentos.get(id)
                peso.append(dic["peso"])
                vectorsDocumentos.update({id:peso})
    return vectorsDocumentos

vec = getVectorsFromFile("calc_pesos_verbose.json")

#for key in vec:
#    print(vec.get(key))
print(vec.get(1))