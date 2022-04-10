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
    

def scrapper(url,cant_paginas, nombre_archivo):
    acum = 1
    encabezado = "Marca,Desc_Producto,Precio\n"
    archivo = open(nombre_archivo, "w+")
    archivo.write(encabezado)
    while (acum <= cant_paginas):
        url = url + '&page='+str(acum)
        uClient = uReq(url)
        sopa_html = soup(uClient.read(), "html.parser")
        uClient.close()
        datos = sopa_html.findAll("div", {"class": "item-container"})
        guardarArchivo(datos,archivo)
        acum = acum+1
        print("Leyendo Pagina # "+str(acum)+ " de "+str(cant_paginas))
    archivo.close()
    

def request(item_name, amount_pages, nombre_archivo):
    url = "https://www.newegg.com/p/pl?d="+item_name
    scrapper(url,amount_pages,nombre_archivo)

if __name__ == '__main__':
    request("GPU",10,"GPU.csv")
