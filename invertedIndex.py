def mergeDocuments(hashMap):
    '''
    En esta funcion se recibe un hast con todos los documentos
    en un diccionario y los pone un una lista uno detras de otro
    '''
    result = []
    for key in hashMap.keys():
        documents = hashMap[key]
        result = result + documents
    return result


def invertIndex(hashMap={}, query=["ATX", "Mid-Tower"]):
    '''
    Se recibe el diccionario con los documentos y una lista que trae
    las palabras a consultar
    '''
    invertedIndex = {}
    #Se deja cada palabra de la consulta en minuscula
    query = [word.lower() for word in query]
    #Generar una lista con todos los documentos
    documents = mergeDocuments(hashMap)
    #Por cada documento en la lista
    for index in range(len(documents)):
        document = documents[index]
        if len(document) > 0 and not isinstance(document[0], str):
            continue
        document = [word.lower() for word in document]
        #convertir todas las palabtas del documento en minuscula
        for queryWord in query:
            #por cada palabra de la consulta se revisa si esta en un documento
            #y se agrega la informacion para crear el indice invertido
            if queryWord in document:
                newOrOldList = invertedIndex[queryWord] if queryWord in invertedIndex else []
                invertedIndex[queryWord] = newOrOldList + [index+1]

    return invertedIndex, documents
