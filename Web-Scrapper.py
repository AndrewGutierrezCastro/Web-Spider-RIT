import schedule
import time
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
        if activar_espera:
            time.sleep(espera_segundos)
            print("Esperando..." +str(espera_segundos)+ "segundos")
        url = url + '&page='+str(acum)
        sopa_html = obtener_html(url)
        datos = sopa_html.findAll("div", {"class": "item-container"})
        guardarArchivo(datos,archivo)
        print(url)
        print("Leyendo Pagina # "+str(acum)+ " de "+str(cant_paginas))
        acum = acum+1
    archivo.close()

def obtener_html(url):
    uClient = uReq(url)
    sopa_html = soup(uClient.read(), "html.parser")
    uClient.close()
    return sopa_html

def request(item_name, amount_pages, nombre_archivo):
    url = "https://www.newegg.com/p/pl?d="+item_name
    scrapper(url,amount_pages,nombre_archivo,True,100)

def main():
    urls = ["MotherBoard", "CPU","GPU", "RAM", "CASE", "PSU", "SSD", "HDD"]

    for part_name in urls:
        request(part_name, 2, part_name+".csv")

if __name__ == '__main__':
    schedule.every().monday().do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
