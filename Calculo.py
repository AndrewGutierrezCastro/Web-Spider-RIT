import numpy as np

'''
    Funcion de calculo de peso, el cual calcula los pesos de un termino en un documento y de un documento en la coleccion
    Tipo_IDF: unaria,suavizada,maxima,probabilistica,inversa
    Tipo_TF: binario, logaritmica, doble, k, frecuencia
    Frequencia: La frequencia de un termino en un documento
    Max(i): Cantidad de terminos en un documento
    Lista_Documentos: una lista con todos los documentos en la coleccion.
    Lista_Documentos_Encontrados: una lista con los documentos donde aparece el termino
    Args: tipo_idf(String), tipo_tf(String), frequencia(Int), maxi(Int), lista_documentos(List),lista_documentos_encontrados(List)
    Return: Int
'''
def calc_peso(tipo_idf, tipo_tf, freq,maxi,lista_documentos,lista_docus_encontrado):
    return calc_peso(tipo_idf,tipo_tf,freq,1,maxi,lista_documentos,lista_docus_encontrado)
'''
    Funcion de calculo de peso, el cual calcula los pesos de un termino en un documento y de un documento en la coleccion
    Tipo_IDF: unaria,suavizada,maxima,probabilistica,inversa
    Tipo_TF: binario, logaritmica, doble, k, frecuencia
    Frequencia: La frequencia de un termino en un documento
    Max(i): Cantidad de terminos en un documento
    Lista_Documentos: una lista con todos los documentos en la coleccion.
    Lista_Documentos_Encontrados: una lista con los documentos donde aparece el termino
    K: Una constante cualquierda
    Args: tipo_idf(String), tipo_tf(String), frequencia(Int), K(Int), maxi(Int), lista_documentos(List),lista_documentos_encontrados(List)
    Return: Int
'''
def calc_peso(tipo_idf, tipo_tf, freq,k,maxi,lista_documentos,lista_docus_encontrado):
    resultado = calc_idf(tipo_idf,lista_documentos,lista_docus_encontrado,maxi) * calc_tf(tipo_tf,freq,k,maxi)
    return resultado
'''
    Funcion de calculo tf, el cual da la importancia del termino en el documento
    Tipo: binario, logaritmica, doble, k, frecuencia
    Frequencia: La frequencia de un termino en un documento
    Max(i): Cantidad de terminos en un documento
    Args: tipo(String), frequencia(Int), maxi(Int)
    Return: Int
'''
def calc_tf(tipo,freq,maxi):
    return calc_tf(tipo,freq,1,maxi)

'''
    Funcion de calculo tf, el cual da la importancia del termino en el documento
    Tipo: binario, logaritmica, doble, k, frecuencia
    Frequencia: La frequencia de un termino en un documento
    K: Una constante cualquierda
    Max(i): Cantidad de terminos en un documento
    Args: tipo(String), frequencia(Int), k(Int), maxi(Int)
    Return: Int
'''
def calc_tf(tipo,freq,k,maxi):
    if tipo =="binario" :
        resultado = calc_tf_bin(freq)
    elif tipo == "logaritmica":
        resultado = calc_tf_log(freq)
    elif tipo == "doble":
        resultado = calc_tf_double(freq,maxi)
    elif tipo ==  "k":
        resultado = calc_tf_double_k(freq,maxi,k)
    else:
        resultado = calc_tf_freq(freq)
    return resultado

'''
    Funcion de calculo tf Binaria, el cual da la importancia del termino en el documento
    Frequencia: La frequencia de un termino en un documento
    Args: frequencia(Int)
    Return: Int
'''
def calc_tf_bin(freq):
    if freq > 0:
        resultado = 1
    else:
        resultado = 0
    return resultado
'''
    Funcion de calculo tf Frequencia, el cual da la importancia del termino en el documento
    Frequencia: La frequencia de un termino en un documento
    Args: frequencia(Int)
    Return: Int
'''
def calc_tf_freq(freq):
    resultado = freq
    return resultado
'''
    Funcion de calculo tf Normalizacion Logaritmica, el cual da la importancia del termino en el documento
    Frequencia: La frequencia de un termino en un documento
    Args: frequencia(Int)
    Return: Int
'''
def calc_tf_log(freq):
    resultado = 1 + np.log2(freq)
    return resultado

'''
    Funcion de calculo tf Normalizacion Doble 0.5, el cual da la importancia del termino en el documento
    Frequencia: La frequencia de un termino en un documento
    Max(i): Cantidad de terminos en un documento
    Args: frequencia(Int), maxi(Int)
    Return: Int
'''
def calc_tf_double(freq,maxi):
    resultado = 0.5+0.5 * (freq/ ( maxi * freq ))
    return resultado
'''
    Funcion de calculo tf Normalizacion Doble 0.5, el cual da la importancia del termino en el documento
    Frequencia: La frequencia de un termino en un documento
    Max(i): Cantidad de terminos en un documento
    K: Una constante cualquierda
    Args: frequencia(Int), maxi(Int), K(Int)
    Return: Int
'''
def calc_tf_double_k(freq,maxi,k):
    resultado = k + (1-k) * ( freq / ( maxi * freq ))
    return resultado

'''
    Funcion de calculo idf, el cual da la especifidad del termino en la coleccion
    Tipo: unaria, suavizada, maxima, probabilistica, inversa
    Lista_Documentos: una lista con todos los documentos en la coleccion.
    Lista_Documentos_Encontrados: una lista con los documentos donde aparece el termino
    Args: tipo(String), lista_documentos(List),lista_documentos_encontrados(List)
    Return: Int
'''
def calc_idf(tipo,list_docus,lista_docus_encontrado):
    return calc_idf(tipo,list_docus,lista_docus_encontrado,1)


'''
    Funcion de calculo idf, el cual da la especifidad del termino en la coleccion
    Tipo: unaria,suavizada,maxima,probabilistica,inversa
    Lista_Documentos: una lista con todos los documentos en la coleccion.
    Lista_Documentos_Encontrados: una lista con los documentos donde aparece el termino
    Cant_Terminos: es la cantidad de terminos en un documento
    Args: tipo(String), lista_documentos(List),lista_documentos_encontrados(List),cantidad_terminos(Int)
    Return: Int
'''
def calc_idf(tipo,list_docus,lista_docus_encontrado,cant_terminos):
    cant_documentos = len(list_docus)
    cant_doccumentos_encontrado = len(lista_docus_encontrado)
    maxi = cant_terminos
    if tipo =="unaria" :
        resultado = calc_idf_unaria()
    elif tipo == "suavizada":
        resultado = calc_idf_inversa_suavi(cant_documentos,cant_doccumentos_encontrado)
    elif tipo == "maxima":
        resultado = calc_idf_inversa_max(cant_doccumentos_encontrado,maxi)
    elif tipo ==  "probabilistica":
        resultado = calc_idf_inversa_prob(cant_documentos,cant_doccumentos_encontrado)
    else:
        resultado = calc_idf_inversa(cant_documentos,cant_doccumentos_encontrado)
    return resultado
'''
    Funcion IDF Unaraia, donde siempre retorna 1
    Args:
    Return: Int
'''
def calc_idf_unaria():
    resultado = 1
    return resultado

'''
    Funcion IDF de Frequencia Inversa.
    Cantidad_Documentos: La cantidad de documentos en la coleccion.
    Cantidad_Documentos_Encontrados: La cantidad de documentos donde aparece el termino.
    Args:Cantidad_Documentos(Int), Cantidad_Documentos_Encontrados(Int)
    Return: Int
'''
def calc_idf_inversa(cant_documentos,cant_doccumentos_encontrado):
    resultado = np.log2( cant_documentos / cant_doccumentos_encontrado )
    return resultado

'''
    Funcion IDF de Frequencia Inversa Suavizada.
    Cantidad_Documentos: La cantidad de documentos en la coleccion.
    Cantidad_Documentos_Encontrados: La cantidad de documentos donde aparece el termino.
    Args:Cantidad_Documentos(Int), Cantidad_Documentos_Encontrados(Int)
    Return: Int
'''
def calc_idf_inversa_suavi(cant_documentos,cant_doccumentos_encontrado):
    resultado = np.log2(1 + ( cant_documentos / cant_doccumentos_encontrado ))
    return resultado

'''
    Funcion IDF de Frequencia Inversa Maxima.
    Cantidad_Documentos_Encontrados: La cantidad de documentos donde aparece el termino.
    Max(i): La cantidad de terminos 
    Args:Cantidad_Documentos(Int), Cantidad_Documentos_Encontrados(Int)
    Return: Int
'''
def calc_idf_inversa_max(cant_doccumentos_encontrado,maxi):
    resultado = np.log2(1 + ((( cant_doccumentos_encontrado * maxi) / cant_doccumentos_encontrado )))
    return resultado

'''
    Funcion IDF de Frequencia Inversa Probabilistica.
    Cantidad_Documentos: La cantidad de documentos en la coleccion.
    Cantidad_Documentos_Encontrados: La cantidad de documentos donde aparece el termino.
    Args:Cantidad_Documentos(Int), Cantidad_Documentos_Encontrados(Int)
    Return: Int
'''
def calc_idf_inversa_prob(cant_documentos,cant_doccumentos_encontrado):
    resultado = np.log2(( cant_documentos - cant_doccumentos_encontrado ) / cant_doccumentos_encontrado )
    return resultado


'''
    Funcion de Calculo de Similitud entre un documento y la consulta.
    vector_documento: Un vector con los pesos de los terminos del documento.
    vector_consulta: Un vector con los pesos de los terminos de la consulta.
    Args:vector_documento(<Vec>), vector_consulta(<Vec>)
    Return: Int
'''
def calc_sim(vector_documento, vector_consulta):
    tam_vec_docu = len(vector_documento)
    tam_vec_cons = len(vector_consulta)
    vector_documento = np.positive(vector_documento)
    vector_consulta = np.positive(vector_consulta)
    if tam_vec_docu > tam_vec_cons:
        vector_documento = vector_documento[:tam_vec_cons]
    elif tam_vec_docu < tam_vec_cons:
        vector_consulta = vector_consulta[:tam_vec_docu]
    #resultado = np.dot(vector_documento,vector_consulta)
    #resultado = np.dot(vector_documento,vector_consulta) / (tam_vec_cons*tam_vec_docu)
    resultado = np.dot(vector_documento,vector_consulta) / (sum(vector_consulta) * sum(vector_documento))
    
    return resultado
