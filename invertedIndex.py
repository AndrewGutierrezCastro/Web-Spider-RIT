def mergeDocuments(hashMap):
    '''
    En esta funcion se recibe un hash con todos los documentos
    en un diccionario y los pone un una lista uno detras de otro
    '''
    result = []
    vocabulary = []
    for key in hashMap.keys():
        documents = hashMap[key]
        result = result + documents
        for document in documents:
            document = [word.lower() for word in document]
            vocabulary += document
    return result, set(vocabulary)
    


def invertIndex(hashMap={}):
    '''
    Se recibe el diccionario con los documentos y una lista que trae
    las palabras a consultar
    '''
    invertedIndex = {}
    # Generar una lista con todos los documentos
    documents, vocabulary = mergeDocuments(hashMap)
    print(len(vocabulary), " terms in the vocabulary.")
    print(len(documents), " documents in the collection.")
    
    # Por cada documento en la lista
    for index in range(len(documents)):
        document = documents[index]
        if len(document) > 0 and not isinstance(document[0], str):
            print(document)
            continue
        document = [word.lower() for word in document]
        # convertir todas las palabtas del documento en minuscula
        for word in vocabulary:
            # por cada palabra de la consulta se revisa si esta en un documento
            # y se agrega la informacion para crear el indice invertido
            if word in document:
                newOrOldList = invertedIndex[word] if word in invertedIndex else []
                timesWordInDocument = [index + 1] * document.count(word)
                invertedIndex[word] = newOrOldList + timesWordInDocument
    return invertedIndex, documents
