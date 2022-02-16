#--------------------------------------------
# IMPORTS
#--------------------------------------------

import numpy as np
import pandas as pnd
import math

#--------------------------------------------
# FUNCIONES
#--------------------------------------------

def calcminmax(observaciones):
    lista_ordenada = observaciones.sort_values(by="NOTAS", axis=0)
    lista_ordenada = lista_ordenada.reset_index(drop=True)
    return lista_ordenada['NOTAS'][0], lista_ordenada['NOTAS'][len(lista_ordenada)-1]

def mediaAritmetica(observaciones):
    valores = observaciones['NOTAS']
    n = valores.count()
    media = 0

    if n > 0:
        for val in valores:
            media += val
        media = media / n

    return media

def medianaDatos(observaciones):
    lista_ordenada = observaciones.sort_values(by="NOTAS", axis=0)
    lista_ordenada = lista_ordenada.reset_index(drop=True)
    n = observaciones['NOTAS'].count()
    mitad = math.trunc(n/2) - 1

    if n % 2 == 1:
        mitad += 1
        return lista_ordenada['NOTAS'][mitad]
    else:
        desfase = lista_ordenada['NOTAS'][mitad+1] - lista_ordenada['NOTAS'][mitad]
        mediana = lista_ordenada['NOTAS'][mitad] + desfase
        return mediana

def counterModa(observaciones):
    valores = observaciones['NOTAS']
    dictionary = {}
    s_dictionary = {}
    # Initialize
    for val in valores:
        dictionary[val] = 0

    #Count
    for val in valores:
        if val in dictionary:
            dictionary[val] += 1

    #Sort
    for val in sorted(dictionary, key=dictionary.get, reverse=True):
        s_dictionary[val] = dictionary[val]

    return s_dictionary

def calVarianza(observaciones, n, media):
    varianza = 0
    valores = observaciones['NOTAS']
    for val in valores:
        varianza += (val - media)**2
    return varianza/(n-1)

def calcularCuartiles(observaciones, n):
    Q1, Q2, Q3 = round(n/4)-1, round(n/2)-1, round((n*3)/4)-1
    valoresOrdenados = observaciones.sort_values(by=['NOTAS'], axis=0)
    valoresOrdenados = valoresOrdenados.reset_index(drop=True)
    valores = list(valoresOrdenados['NOTAS'])

    valQ1 = (valores[Q1] + ((valores[Q1 + 1] - valores[Q1]) / 2) + valores[Q1 + 1])/2 if Q1 % 2 == 1 else valores[Q1]
    valQ2 = (valores[Q2] + ((valores[Q2 + 1] - valores[Q2]) / 2) + valores[Q2 + 1])/2 if Q2 % 2 == 1 else valores[Q2]
    valQ3 = (valores[Q3] + ((valores[Q3 + 1] - valores[Q3]) / 2) + valores[Q3 + 1])/2 if Q3 % 2 == 1 else valores[Q3]

    return valQ1, valQ2, valQ3


#--------------------------------------------
# APLICACION
#--------------------------------------------

observaciones = pnd.DataFrame({"NOTAS": np.array([3, 19, 10, 15, 14, 12, 9, 8, 11, 12, 11, 12, 13, 11, 14, 16])})
caracteristicas = observaciones.count()
print(str(observaciones))
print("Caracteristicas = " + str(caracteristicas))
min, max = calcminmax(observaciones)

print("MIN " + str(min))
print("MAX " + str(max))


print("Rango " + str(max-min))

media = mediaAritmetica(observaciones)

print("Media aritmetica " + str(media))

mediana = medianaDatos(observaciones)

print("Mediana " + str(mediana))

moda_ordenada = counterModa(observaciones)
first_element = list(moda_ordenada.values())[0]
#result = dict(((v, k) for k in mydict for v in mydict[k] if v in required))
moda_lista = list(k for k in list(moda_ordenada.keys()) if moda_ordenada.get(k) == first_element)
print('MODA ' + str(moda_lista))

varianza = calVarianza(observaciones, caracteristicas, media)
print('Varianza ' + str(varianza))

desv_tipica = math.sqrt(varianza)

print('Desv. Tipica ' + str(round(desv_tipica, 2)))
quart = calcularCuartiles(observaciones, int(caracteristicas))
print("El 25% de las observaciones tiene una nota inferior a " + str(quart[0]))
print("El 50% de las observaciones tiene una nota alrededor de " + str(quart[1]))
print("El 75% de las observaciones tiene una nota inferior a " + str(quart[2]))
print("Las notas del 25% más bajas se diferencias de las del 25% más altas por " + str(quart[2] - quart[0]) + " puntos")

