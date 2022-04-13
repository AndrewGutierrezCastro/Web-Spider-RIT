from tracemalloc import start
import schedule
import time
import random
import threading
from bs4 import BeautifulSoup as soup  # Lector HTML
from urllib.request import urlopen as uReq  # Web client

def guardarArchivo(datos,archivo):
    for dato in datos:
        informacionParseada = parser(dato)
        archivo.write(informacionParseada)

def parser(dato):
    informacion = dato.find("a",class_="item-title").text.split(' ',1)
    try:
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
    resultado = marca + ", " + desc_producto.replace(",", "|") + ", " +precio.replace(",", "") +"\n"
    return resultado
    
    
def scrapper(url,cant_paginas, nombre_archivo,activar_espera,espera_segundos):
    acum = 1
    encabezado = "Marca,Desc_Producto,Precio\n"
    archivo = open(nombre_archivo, "w+")
    archivo.write(encabezado)
    while (acum <= cant_paginas):
        url = url + '&page='+str(acum)
        sopa_html = obtener_html(url)
        datos = sopa_html.findAll("div", {"class": "item-container"})
        guardarArchivo(datos,archivo)
        print(url)
        print("Leyendo Pagina # "+str(acum)+ " de "+str(cant_paginas))
        acum = acum+1
        if activar_espera and acum <= cant_paginas:
            print("Esperando..." +str(espera_segundos)+ "segundos")
            time.sleep(espera_segundos)
    archivo.close()

def obtener_html(url):
    uClient = uReq(url)
    sopa_html = soup(uClient.read(), "html.parser")
    uClient.close()
    return sopa_html

def request(item_name, amount_pages, nombre_archivo):
    url = "https://www.newegg.com/p/pl?d="+item_name
    activar_espera = True
    esperar_segundos = 25
    scrapper(url,amount_pages,nombre_archivo,activar_espera,esperar_segundos)

def main():
    print("---------Corriendo Programa---------")
    cant_paginas = 2
    urls = ["MotherBoard", "CPU","GPU", "RAM", "CASE", "PSU", "SSD", "HDD"]
    for part_name in urls:
        rand_segundos = random.randrange(0,10)
        time.sleep(rand_segundos)
        proceso = threading.Thread(target =request, args=(part_name, cant_paginas, part_name+".csv"))
        proceso.start()
    proceso.join()
    print("---------Programa Terminado---------")

if __name__ == '__main__':
    #schedule.every().monday.do(main)
    schedule.every(5).to(10).minutes.do(main)
    while True:
        print("---------Esperando a correr el programa---------")
        schedule.run_pending()
        segundos_faltantes = schedule.idle_seconds()
        print(str(schedule.get_jobs()))
        print("---------Faltan: " +str(round(segundos_faltantes))+ " segundos---------")
        time.sleep(round(segundos_faltantes/5))
