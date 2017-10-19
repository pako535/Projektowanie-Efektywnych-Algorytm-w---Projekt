from numpy import*
import linecache
import sys
import math

def creatematrix():

    file = 'gr17.tsp'
    tekst = open(file).read()
    # print(tekst)
    tekst = tekst.split()
    tekst = tekst[15:]
    # print(tekst)

    dl = len(tekst)

    dimension = linecache.getline(file, 4)
    dimension = dimension[11:]
    dimension = int(dimension)

    tab = zeros((dimension, dimension), int)
    # print(tab)

    # wpisywanie do macierzy odległosci jako int a nie str
    counter = 0

    infinity = -1

    for i in range(dimension):
        j = 0
        k = False
        while(True):
            if tekst[counter] == '0':
                tekst[counter] = infinity
            tab[i][j] = int(tekst[counter])
            tab[j][i] = int(tekst[counter])
            counter += 1
            j += 1
            k = True
            if not(tekst[counter - 1] != infinity and counter - 1 < dl):
                break

        if k == False:
             counter += 1
    #print(tab)
    return tab


