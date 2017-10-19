import macierz



#
#
#   Warunek do spełnienia w każdej kolumnie i każdym wierszu musi znajdywać się zero, więc jesli
#   po odjęciu wierszy jakaś kolumna lub wiersz nie ma zera, to w danym wierszu lub kolumnie trzeba odjac minimum juz po
#   wczesniejszego wiersza
#
#   Brak usuwania odpowiednich kolumn i wierszy
#
#






# Wykorzystuje metode Litte'a (1962) dla algorytmu podziału i ograniczeń
class Komiwojazer:


    def __init__(self , tab):
        self.tab = tab
        self.count_row = len(self.tab[:, 1])
        self.list_of_min_in_row = []
        self.value_of_low_band = 0


    # Przy obliczaniu low band dla macierzy antysymetrycznej trzeba uwzględnić jeszcze pioneowe minima wg pkt b
    def low_bound(self):

        #jesli lista minimów jest pełna to usuń by uzupełnić od nowa
        if self.list_of_min_in_row:
            del self.list_of_min_in_row[ : ]

                                                                                                            #count_row = len(self.tab[:, 1])
        #Przeszukanie wierszy w celu szukania minimum oraz odfiltrowanie 0
        for i in range(self.count_row):
            self.list_of_min_in_row.append(min(filter(lambda x:x>0 ,self.tab[i, :])))

                                                                                                                        #list_of_min_in_colum = []
                                                                                                                        # Przeszukanie kolumn w celu szukania minimum oraz odfiltrowanie 0, dla antysymetrycznych macierzy
                                                                                                                   # for i in range(count_row):
                                                                                                                        #     list_of_min_in_colum.append(min(filter(lambda x:x>0 ,self.tab[:, i])))
        self.value_of_low_band = sum(self.list_of_min_in_row)

        #odejmowanie w wierszach
        for i in range(self.count_row):
            for j in range(self.count_row):
                if self.tab[i, j] > 0:
                    self.tab[i, j] = self.tab[i, j] - self.list_of_min_in_row[i]

        #print('\n', self.list_of_min_in_row)

        return self.value_of_low_band

    # funkcja szukająca dodatniego minimum większego od zera, chyba że w danym wierszu lub kolumnie zero występi więcej
    # niż raz

    def my_min(self, tab):

        if tab[0] < 0:
            min = tab[1]
        else:
            min = tab[0]

        flag = False
        for i in tab:
            if i > 0 and min > i:
                min = i
            if flag == True and min > i and i >= 0:
                min = i
            if i == 0:
                 flag = True

        #print("\nMoje minimum: ", min)
        return min



    def find_min_in_row_and_column(self):

        list_of_min_in_row = []
        list_of_min_in_column = []


        for i in range(self.count_row):
            list_of_min_in_row.append(self.my_min(self.tab[i, :]))

        for i in range(self.count_row):
            list_of_min_in_column.append(self.my_min(self.tab[:, i]))

        max_row = max(list_of_min_in_row)
        max_column = max(list_of_min_in_column)
        my_max = max(max_row,max_column)

        k = 0
        if max_row == my_max:
            index_row = list_of_min_in_row.index(my_max)
            print("\nIndeks w wierszu: ", index_row)
            k = 1
        else:
            index_column = list_of_min_in_column.index(my_max)
            print("\nIndeks w kolumnie: ", index_column)
            k = 2

        print("\nMax: ", my_max)
        print("\nLista nowych minimów\nWiersze: ", list_of_min_in_row, "\nKolumny: ",list_of_min_in_column)






    def display(self):
        print(self.tab)




