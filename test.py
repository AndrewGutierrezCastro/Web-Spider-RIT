from itertools import groupby
import json

import collections
from typing import Collection
from invertedIndex import invertIndex  # Recipiente de archivos

def calc_performance(input_file_path):
    with open(input_file_path, 'r') as j:
        contents = json.load(j)
    for key in contents:
        value = contents[key]
        print("The key and value are ({})".format(key))
        repeated_elements = [item for item, count in collections.Counter(value).items() if count > 1]
        numbered_list = collections.Counter(value)
        print(numbered_list)
        amount_repeated_list = {}
        for repeated_elemnt in repeated_elements:
            amount_repeated_list[repeated_elemnt] = numbered_list[repeated_elemnt]
        #print(amount_repeated_list)
    frequency = numbered_list
    #maxi = 
    #list_documents =
    #list_documents_found =
    #k = 
    #calc_peso()
    #print(data)
    return 0
calc_performance("invertedIndex.json")