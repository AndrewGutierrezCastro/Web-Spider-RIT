filename = "calc_performance_verbose.txt"

# Lee el archivo y obtiene e contenido
f = open(filename, 'r')
mytext = f.read()

# Convierte el contenido a binario y lo encodifica
binarytxt = str.encode(mytext)

# Guarda el contenido codificado binario en un archivo binario
with open('calc_performance_verbose_binary', 'wb') as fbinary:
    fbinary.write(binarytxt)