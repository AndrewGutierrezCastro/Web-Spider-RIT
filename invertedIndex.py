def mergeDocuments(hashMap):
    result = []
    for key in hashMap.keys():
        documents = hashMap[key]
        result = result + documents
    return result


def invertIndex(hashMap={}, query=["ATX", "Mid-Tower"]):
    invertedIndex = {}
    query = [word.lower() for word in query]

    documents = mergeDocuments(hashMap)

    for index in range(len(documents)):
        document = documents[index]
        if len(document) > 0 and not isinstance(document[0], str):
            continue
        document = [word.lower() for word in document]

        for queryWord in query:
            if queryWord in document:
                newOrOldList = invertedIndex[queryWord] if queryWord in invertedIndex else []
                invertedIndex[queryWord] = newOrOldList + [index+1]

    return invertedIndex, documents
