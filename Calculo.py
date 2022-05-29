import numpy as np
import glob
import os

def calc_idf(list_resultados,extencion):
    locacion2 = os.getcwd()+"/*."+extencion
    list_docus =glob.glob(locacion2)
    cant_docus = len(list_docus)
    cant_result =len(list_resultados)
    resultado = np.log2(cant_docus/cant_result)
    return resultado

def calc_tf(tipo,freq):
    return calc_tf(tipo,freq,1)

def calc_tf(tipo,freq,k):
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

def calc_tf_bin(freq):
    resultado = 0
    return resultado

def calc_tf_freq(freq):
    resultado = freq
    return resultado

def calc_tf_log(freq):
    resultado = 1 + np.log2(freq)
    return resultado

def calc_tf_double(freq,maxi):
    resultado = 0.5+0.5 * (freq/ ( maxi * freq ))
    return resultado

def calc_tf_double_k(freq,maxi,k):
    resultado = k + (1-k) * ( freq / ( maxi * freq ))
    return resultado


def calc_idf(tipo,freq,k):
    
    locacion2 = os.getcwd()+"/*."+extencion
    list_docus =glob.glob(locacion2)
    
    cant_docus = len(list_docus)
    cant_result =len(list_resultados)

    if tipo =="unaria" :
        resultado = calc_idf_unaria()
    elif tipo == "suavizada":
        resultado = calc_idf_inversa_suavi()
    elif tipo == "maxima":
        resultado = calc_idf_inversa_max(freq,maxi)
    elif tipo ==  "probabilistica":
        resultado = calc_idf_inversa_prob(freq,maxi,k)
    else:
        resultado = calc_idf_inversa(freq)
    return resultado

def calc_idf_unaria():
    resultado = 1
    return resultado

def calc_idf_inversa(cant_documentos,cant_doccumentos_encontrado):
    resultado = np.log2( cant_documentos / cant_doccumentos_encontrado )
    return resultado

def calc_idf_inversa_suavi(cant_documentos,cant_doccumentos_encontrado):
    resultado = np.log2(1 + ( cant_documentos / cant_doccumentos_encontrado ))
    return resultado

def calc_idf_inversa_max(cant_doccumentos_encontrado,maxi):
    resultado = np.log2(1 + ((( cant_doccumentos_encontrado * maxi) / cant_doccumentos_encontrado )))
    return resultado

def calc_idf_inversa_prob(cant_documentos,cant_doccumentos_encontrado,maxi):
    resultado = np.log2(( cant_documentos - cant_doccumentos_encontrado ) / cant_doccumentos_encontrado )
    return resultado

print(calc_idf([2,3,4],"csv"))