from bs4 import BeautifulSoup as soup  # Lector HTML
from urllib.request import urlopen as uReq  # Web client

def guardarArchivo(datos,encabezado,archivo):
    for dato in datos:
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
        pos_gb = informacion[1].find("GB")
        cant_ram = informacion[1][pos_gb-1]
        if(not(cant_ram.isdigit())):
            cant_ram = "0"
        print("Marca: " + marca + "\n")
        print("Desc_Producto: " + desc_producto + "\n")
        print("Cant_Ram: " + cant_ram + "\n")
        print("Precio: " + precio + "\n")
        archivo.write(marca + ", " + desc_producto.replace(",", "|") + ", " + cant_ram +", " +precio.replace(",", "") +"\n")
    #print(dato)
    

def scrapper(url,cant_paginas):
    acum = 1
    archivo_guardado = "articulos.csv"
    encabezado = "Marca,Desc_Producto,Cant_Ram,Precio\n"
    archivo = open(archivo_guardado, "w")
    while (acum <= cant_paginas):
        url = url + '&page='+str(acum)
        uClient = uReq(url)
        sopa_html = soup(uClient.read(), "html.parser")
        uClient.close()
        datos = sopa_html.findAll("div", {"class": "item-container"})
        guardarArchivo(datos,encabezado,archivo)
        acum = acum+1
        print("Leyendo Pagina #"+str(acum)+ "de "+str(cant_paginas))
    archivo.close()
    

def test():
    url = "https://www.newegg.com/p/pl?d=GPU&page=1"
    uClient = uReq(url)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    
    

def main():
    #url = "http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=GTX&bop=And&Page=1&PageSize=36&order=BESTMATCH"
    #url = "https://www.newegg.com/p/pl?d=GPU&page=1"
    url = "https://www.newegg.com/p/pl?d=GPU"
    scrapper(url,100)
    #test()

if __name__ == '__main__':
    main()
