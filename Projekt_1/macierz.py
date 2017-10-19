from numpy import*
import linecache


def creatematrix():

    file = 'gr17.tsp'
    tekst = open(file).read()
    print(tekst)
    tekst = tekst.split()
    tekst = tekst[15:]
    print(tekst)

    dl = len(tekst)

    dimension = linecache.getline(file, 4)
    dimension = dimension[11:]
    dimension = int(dimension)

    tab = zeros((dimension, dimension), int)
    # print(tab)

    # wpisywanie do macierzy odległosci jako int a nie str
    licznik = 0
    for i in range(dimension):
        j = 0
        k = False
        while(True):
            tab[i][j] = int(tekst[licznik])
            tab[j][i] = int(tekst[licznik])
            licznik += 1
            j += 1
            k = True
            if not(tekst[licznik - 1] != '0' and licznik - 1 < dl):
                break

        if k == False:
             licznik += 1

    print(tab)
    return tab


