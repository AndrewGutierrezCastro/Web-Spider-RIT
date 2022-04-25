from tracemalloc import start
import schedule #Liberia para manejar el scheduler 
import time #Liberia para poder hacer waiting.
import random
import threading #Liberia para poder manejar los threads
from bs4 import BeautifulSoup as soup  # Lector HTML
from urllib.request import urlopen as uReq  # Web client

#Funcion que se encarga de guardar datos en un archivo.
#Entra como argumento un string de dato, y un archvio al cual se le concatenara los datos.
def guardarArchivo(datos,archivo):
    for dato in datos:
        informacionParseada = parser(dato)
        archivo.write(informacionParseada)


#Funcion se encarga de extraer los datos necesarios del html obtenido
#Entra como argumento el codigo html extraido de la pagina.
#Sale un String con solo los datos necesario con formatio compatible con csv
def parser(dato):
    
    informacion = dato.find("a",class_="item-title").text.split(' ',1)
    try:
        url_producto = dato.find("a",class_="item-img").get("href")
        info_producto = dato.findAll("div", {"class": "item-info"})
        info_precio = info_producto[0].findAll("ul",{"class":"price"})
        if(len(info_precio) > 0):
            precio = info_precio[0].findAll("li",{"class":"price-current"})[0].findAll("strong")[0].text
        else:
            info_producto = dato.findAll("div", {"class": "item-action"})
            precio = info_producto[0].findAll("ul",{"class":"price"})[0].findAll("li",{"class":"price-current"})[0].findAll("strong")[0].text
    except:
        precio = 'NA'
    marca = informacion[0]
    desc_producto = informacion[1]

    print("Marca: " + marca + "\n")
    print("Desc_Producto: " + desc_producto + "\n")
    print("Precio: " + precio + "\n")
    print("Link " + url_producto + "\n")
    resultado = marca.replace(",", "") + ", " + desc_producto.replace(",", "") + ", " +precio.replace(",", "") + ", " + url_producto + "\n"
    return resultado
    
#Funcion se encarga de extraer codigo html de una pagina, se toma en cuenta la posibilidad de
#poder esperar x cantidad de segundos antes de iniciar la siguiente extraccion.
#Entra como argumento, el URL de la pagina en formato string, cantidad de paginas en formato int,
#Nombre del archivo al cual se guardara la informacion en formato String, Activacion de espera en formato bool.
#Y Espera de segundos en formato Int.
def scrapper(url,cant_paginas, nombre_archivo,activar_espera,espera_segundos):
    acum = 1
    encabezado = "Marca,Desc_Producto,Precio,URL_Producto\n"
    archivo = open(nombre_archivo, "w+")
    archivo.write(encabezado)
    while (acum <= cant_paginas):
        url_temp = url+str(acum)
        sopa_html = obtener_html(url_temp)
        datos = sopa_html.findAll("div", {"class": "item-container"})
        guardarArchivo(datos,archivo)
        print(url_temp)
        print("Leyendo Pagina # "+str(acum)+ " de "+str(cant_paginas))
        acum = acum+1
        if activar_espera and acum <= cant_paginas:
            print("Esperando..." +str(espera_segundos)+ "segundos")
            time.sleep(espera_segundos)
    archivo.close() # Se cierra el archivo abierto.

#Esta funcion obtiene el codigo html de un url
#Entra como argumento un url de l apagina en formato String
def obtener_html(url):
    uClient = uReq(url)
    sopa_html = soup(uClient.read(), "html.parser")
    uClient.close()
    return sopa_html

#Esta funcion se encarga de darle formato correto al url y de llamar al scraper de manera correcta.
#Se maneja la cantidad e paginas que se quiere obtener.
def request(item_name, amount_pages, nombre_archivo):
    url = "https://www.newegg.com/p/pl?d="+item_name +'&page='
    activar_espera = True
    esperar_segundos = 25
    scrapper(url,amount_pages,nombre_archivo,activar_espera,esperar_segundos)

#Esta funcion se encarga de manejar el levantamiento de los threads, los cuales se hacen en un
#lapso random de segundos para evitar el accesso exesivo de los recursos de la pagina.
def main():
    print("---------Corriendo Programa---------")
    cant_paginas = 60
    urls = ["MotherBoard", "CPU","GPU", "RAM", "CASE", "PSU", "SSD", "HDD"]
    for part_name in urls:
        rand_segundos = random.randrange(0,10)
        time.sleep(rand_segundos)
        proceso = threading.Thread(target =request, args=(part_name, cant_paginas, part_name+".csv"))
        proceso.start()
    proceso.join()
    print("---------Programa Terminado---------")

#Se encarga de asegurar que el unico main que se levante es el mismo, y se manejar los schedules
#Se hace un schedule cada lunes y se impreme el progreso del schedule cada X cantidad de segundos.
if __name__ == '__main__':
    schedule.every().monday.do(main)
    #schedule.every(5).to(10).minutes.do(main)
    while True:
        print("---------Esperando a correr el programa---------")
        schedule.run_pending()
        segundos_faltantes = schedule.idle_seconds()
        print(str(schedule.get_jobs()))
        print("---------Faltan: " +str(round(segundos_faltantes))+ " segundos---------")
        time.sleep(round(segundos_faltantes/5))
