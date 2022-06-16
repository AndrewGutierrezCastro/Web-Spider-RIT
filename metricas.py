#Calculan la precision promedio a un "n" especifico (5, 10, 20)
#Primero, determinan la cantidad de relevantes y despues la
#dividen entre el "n" correspondiente 


def PrecisionProm_n(conjunto_de_resultados, n):
    cant_relevantes = 0
    for doc in conjunto_de_resultados[:n+1]: 
        #if doc.esRelevante:
            cant_relevantes+=1
    P_a_n = cant_relevantes/n
    print(P_a_n)
    return P_a_n



