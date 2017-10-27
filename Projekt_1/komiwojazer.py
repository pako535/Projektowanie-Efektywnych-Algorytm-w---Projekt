import macierz
from collections import namedtuple


#
#
#
#   Brak poprawnego wyszukania maximum dla kolumny i wiersza, następnie dodanie do low band wartości minimalnej,
#   następnie zablokowanie odpowiedniej kolumny lub wiersza.
#                   ||
#                   \/
#   Brak usuwania odpowiednich kolumn i wierszy
#
#






# Wykorzystuje metode Litte'a (1962) dla algorytmu podziału i ograniczeń
class Komiwojazer:


    def __init__(self , tab):
        self.my_struct = namedtuple("my_struct",['value','x','y'])
        self.tab = tab
        self.count_row = len(self.tab[:, 1])
        self.list_of_min_in_row = [self.my_struct]
        self.value_of_low_band = 0
        self.list_of_min_in_colum = [self.my_struct]

    # Przy obliczaniu low band dla macierzy antysymetrycznej trzeba uwzględnić jeszcze pioneowe minima wg pkt b
    def low_bound(self):

        #jesli lista minimów jest pełna to usuń by uzupełnić od nowa
        if self.list_of_min_in_row:
            del self.list_of_min_in_row[ : ]
        if self.list_of_min_in_colum :
            del self.list_of_min_in_colum[ : ]

        #Przeszukanie wierszy w celu szukania minimum oraz odfiltrowanie 0
        for i in range(self.count_row):
            a = (min(filter(lambda x: x > 0, self.tab[i, :])))
            tmp_array = self.tab[i, :].tolist()
            id = tmp_array.index(a)
            p = self.my_struct(a, i,id)
            self.list_of_min_in_row.append(p)



        #odejmowanie w wierszach
        for i in range(self.count_row):
            for j in range(self.count_row):
                if self.tab[i][j] > 0:
                    self.tab[i][j] = self.tab[i][j] - self.list_of_min_in_row[i][0]
            #print(self.list_of_min_in_row[i][0])



        # Przeszukanie kolumn w celu szukania minimum oraz odfiltrowanie 0
        for i in range(self.count_row):
            a = (min(filter(lambda x: x >= 0, self.tab[:, i])))
            tmp_array = self.tab[:, i].tolist()
            id = tmp_array.index(a)
            p = self.my_struct(a, i, id)
            self.list_of_min_in_colum.append(p)



        # odejmowanie w kolumnach
        for i in range(self.count_row):
            for j in range(self.count_row):
                if self.tab[j][i] > 0:
                    self.tab[j][i] = self.tab[j][i] - self.list_of_min_in_colum[i][0]

        # Sumowanie wartosci ograniczenia
        #self.value_of_low_band = sum(self.list_of_min_in_row[:][0]) + sum(self.list_of_min_in_colum[:][0])

        for i in range(self.count_row):
            self.value_of_low_band += self.list_of_min_in_row[i][0] + self.list_of_min_in_colum[i][0]


        print(self.value_of_low_band)
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


# tutaj skonczyłem
#     def find_max_in_row_and_column(self):
#
#         list_of_min_in_row = []
#         list_of_min_in_column = []
#
#
#         for i in range(self.count_row):
#             list_of_min_in_row.append(self.my_min(self.tab[i, :]))
#
#         for i in range(self.count_row):
#             list_of_min_in_column.append(self.my_min(self.tab[:, i]))
#
#         max_row = max(list_of_min_in_row)
#         max_column = max(list_of_min_in_column)
#         my_max = max(max_row,max_column)
#
#         k = 0
#         if max_row == my_max:
#             index_row = list_of_min_in_row.index(my_max)
#             print("\nIndeks w wierszu: ", index_row)
#             k = 1
#         else:
#             index_column = list_of_min_in_column.index(my_max)
#             print("\nIndeks w kolumnie: ", index_column)
#             k = 2
#
#         print("\nMax: ", my_max)
#         print("\nLista nowych minimów\nWiersze: ", list_of_min_in_row, "\nKolumny: ",list_of_min_in_column)

    # def find_max_and_cut(self):
    #
    #
    #     max = 0
    #     tmpi = 0
    #     tmpj = 0
    #     for i in range(self.count_row):
    #         for j in range(self.count_row):
    #             if self.tab[i][j] > max:
    #                 max = self.tab[i][j]
    #                 tmpi = i
    #                 tmpj = j
    #
    #     print("Maksymalnyelement: ", max, "o indeksach:<", tmpi, ",", tmpj, ">")

    def display(self):
        print(self.tab)




