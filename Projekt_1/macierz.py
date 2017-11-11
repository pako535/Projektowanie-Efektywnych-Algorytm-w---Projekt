from numpy import*
import linecache
import sys
import math

def creatematrix_TSP():



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
            tab[j][i] = -1 #int(tekst[counter])
            counter += 1
            j += 1
            k = True
            if not(tekst[counter - 1] != infinity and counter - 1 < dl):
                break

        if k == False:
             counter += 1
    #print(tab)
    return tab


def creatematrix_ATSP():
    file = 'my4.atsp'
    tekst = open(file).read()

    #print(tekst)
    tekst = tekst.split()
    #print(tekst)
    tekst = tekst[15:]
    #print(tekst)

    dl = len(tekst)

    dimension = linecache.getline(file, 4)
    dimension = dimension[11:]
    dimension = int(dimension)

    tab = zeros((dimension + 1 , dimension + 1 ), int)
    # print(tab)

    # wpisywanie do macierzy odległosci jako int a nie str
    counter = 0

    infinity = -1

    for i in range(dimension):
        for j in range(dimension):
            if tekst[counter] == '100000000':
                tekst[counter] = infinity
            tab[i+1][j+1] = int(tekst[counter])
            counter += 1

    for i in range(dimension):
        tab[0, 1+i:] = i
        tab[1+i :,0] = i
    #print(tab)



    return tab


