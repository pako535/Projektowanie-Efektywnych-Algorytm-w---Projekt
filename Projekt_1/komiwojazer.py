import macierz


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



    def display(self):
        print(self.tab)




