import macierz
from collections import namedtuple
from operator import attrgetter
from numpy import*
import copy

#   Brak usuwania odpowiednich kolumn i wierszy
#
#

#####################################################################################
# NAPISAĆ MECHANIZM KTORY USTAWIA KOSZTY OPTYMALNEGO PRZEJSCIA NA NIESKONCZONOSC ABY PRAWIDŁOWO BYŁ WYBIERANY PUNTK
# KTORY MA BYC DO WYCIECIA
####################################################################################

# Wykorzystuje metode Litte'a (1962) dla algorytmu podziału i ograniczeń
class Komiwojazer:


    def __init__(self , tab):

        self.ABC = namedtuple("ABC", ['value', 'index'])
        self.my_struct = namedtuple("my_struct",['value','x','y'])
        self.tab = tab
        self.element = namedtuple("element", ['tab', 'lower_bound', 'del_x', 'del_y','index'])
        self.list_of_low_bound = []
        self.list_of_branch = []#.append(tab)

        element = self.add_element(tab)
        print(element)

    def my_main(self):
        i = 0

        # self.add_element1(self.list_of_branch[i][0], self.list_of_branch[i][1], i)
        # i =2
        # self.add_element1(self.list_of_branch[i][0], self.list_of_branch[i][1], i)
        # i=15
        # self.add_element1(self.list_of_branch[i][0], self.list_of_branch[i][1], i)
        min = self.list_of_low_bound[0][0]
        self.list_of_low_bound = sorted(self.list_of_low_bound, key=attrgetter('index'))
        for j in range(len(self.list_of_low_bound)):
            if self.list_of_low_bound[j][0] <= min:
                min = self.list_of_low_bound[j][0]
                i = self.list_of_low_bound[j][1]

        # upper_bound = 0         #Najlepszy wynik dotychczas znaleziony
        # tmp_tab = self.tab
        # for i in range(len(tmp_tab)):
        #     try:
        #         a = (min(filter(lambda x: x >= 0, tmp_tab[i, :])))
        #     except ValueError:
        #         pass
        #
        #     upper_bound += a




        # ABC = namedtuple("ABC",['value','index'])
        # a = ABC(self.list_of_branch[0].lower_bound,0)
        # self.list_of_low_bound.append(a)



        #self.add_element(self.list_of_branch[3][0])
        while( len(self.list_of_branch[i][0]) != 2):

            tmp_j = 0
            for j in range(len(self.list_of_low_bound)):
                if self.list_of_low_bound[j][1] == i:
                    tmp_j = j
            self.list_of_low_bound.remove(self.list_of_low_bound[tmp_j])

            self.add_element1(self.list_of_branch[i][0], self.list_of_branch[i][1], i)

            self.list_of_low_bound = sorted(self.list_of_low_bound, key=attrgetter('index'))
            min = self.list_of_low_bound[0][0]
            for j in range(len(self.list_of_low_bound)):
                if self.list_of_low_bound[j][0] != None:
                    if self.list_of_low_bound[j][0] <= min:
                        # if self.list_of_low_bound[j][0] < min:
                        min = self.list_of_low_bound[j][0]
                        i = self.list_of_low_bound[j][1]

        print (i,'\n')
        # print(self.list_of_low_bound)
        for q in range(len(self.list_of_branch)):
            # if self.list_of_branch[i] != None:
            print(q," -element\n",self.list_of_branch[q],"\n")

        print("\n\n\n#### WYNIK :", self.list_of_branch[i],'\n')
    def add_element(self,tab):
        #my_struct = namedtuple("my_struct", ['value', 'x', 'y'])

        ###############################################################################################################
        # Krok 1
        ###############################################################################################################
        count_row = len(tab[:, 1]) - 1

        tmp_tab = copy.copy(tab)
        list_of_min_in_row = self.find_min_in_row(tmp_tab, count_row)
        tmp_tab = self.sub_min_in_row(tmp_tab, count_row, list_of_min_in_row)
        list_of_min_in_column = self.find_min_in_column(tmp_tab, count_row)
        tmp_tab = self.sub_min_in_column(tmp_tab, count_row, list_of_min_in_column)

        value_of_low_band = self.low_bound(list_of_min_in_row, list_of_min_in_column, count_row)

        # Dodanie 0 elementu
        j = len(self.list_of_branch)
        element = self.element(tab, value_of_low_band, None, None, j)
        self.list_of_branch.append(element)

        ###############################################################################################################
        # Krok 2
        ###############################################################################################################

        # Szukanie max kosztu wyłączenia
        # 0 - value, 1 - x ,2 - y
        tuple_max_in_min = self.find_max_opty(tmp_tab)


        #   Dodanie prawego dziecka z zablokowana droga o max opt kosztem wylaczenia

        value_of_low_band += tuple_max_in_min[0]

        tmp_xx = tab[0, :].tolist()
        # zablokowanie
        try:
            px = tmp_xx.index(tuple_max_in_min[2])
            tmp_yy = tab[:, 0].tolist()
            try:
                py = tmp_yy.index(tuple_max_in_min[1])
                tmp_tab[px, py] = -1
                #tab[pyy, pxx] = -1
            except:
                pass
        except:
            pass

        # powiększenie drzewa
        tmp_j = len(self.list_of_branch) - 1
        if j == 0:
            self.list_of_branch.append(None)
            self.list_of_branch.append(None)
        else:
            if j < 2 * j + 2:
                while tmp_j != 2 * j + 2:
                    self.list_of_branch.append(None)
                    tmp_j += 1

        self.list_of_branch[2 * j + 2] = self.element(tmp_tab,value_of_low_band,None, None,2 * j + 2)

        a = self.ABC(self.list_of_branch[2 * j + 2].lower_bound, 2 * j + 2)
        self.list_of_low_bound.append(a)
        ###############################################################################################################
        # Krok 3
        ###############################################################################################################

        # Dodanie lewego wyciętego
        # Wycięcie i zablokowanie drogi powrotnej

        tmp_tab1 = copy.copy(tmp_tab)
        left_child = zeros((len(tab) - 1, len(tab) - 1), int)
        prv_x = tuple_max_in_min[1]
        l = 0
        tmp_xx = tmp_tab1[0, :].tolist()
        try:
            pxx = tmp_xx.index(tuple_max_in_min[1])

            tmp_yy = tab[:, 0].tolist()
            try:
                pyy = tmp_yy.index(tuple_max_in_min[2])
                tmp_tab1[pxx,pyy] = -1
            except:
                pass
        except:
            pass
        for i  in range(len(tmp_tab1)):
            c = 0
            for z in range(len(tmp_tab1)):
                if i != pyy :
                    if z != pxx:
                        left_child[l][c] = tmp_tab1[i][z]

                if z == pxx:
                    c -= 1
                c += 1

            if i == pyy:
                l -= 1
            l += 1

        value_of_low_band -= tuple_max_in_min[0]

        #redukcja wierszy i kolumn
        count_row = len(left_child) - 1

        list_of_min_in_row = self.find_min_in_row(left_child, count_row)
        left_child = self.sub_min_in_row(left_child, count_row, list_of_min_in_row)

        list_of_min_in_column = self.find_min_in_column(left_child, count_row)
        left_child = self.sub_min_in_column(left_child, count_row, list_of_min_in_column)


        value_of_low_band +=  self.low_bound(list_of_min_in_row, list_of_min_in_column, count_row)

        self.list_of_branch[2 * j + 1] = self.element(left_child,value_of_low_band,tuple_max_in_min[1], tuple_max_in_min[2],2 * j + 1)

        ###############################################################################################################
        # Krok 4
        ###############################################################################################################
        ##### Powtórzenie korku 2
        ###############################################################################################################
        j = 2 * j + 1
        # Szukanie max kosztu wyłączenia
        # 0 - value, 1 - x ,2 - y
        tuple_max_in_min = self.find_max_opty(left_child)

        #   Dodanie prawego dziecka z zablokowana droga o max opt kosztem wylaczenia

        value_of_low_band += tuple_max_in_min[0]

        tmp_xx = left_child[0, :].tolist()
        # zablokowanie
        try:
            px = tmp_xx.index(tuple_max_in_min[1])
            tmp_yy = left_child[:, 0].tolist()
            try:
                py = tmp_yy.index(tuple_max_in_min[2])
                left_child[px, py] = -1
                # tab[pyy, pxx] = -1
            except:
                pass
        except:
            pass

        # powiększenie drzewa
        tmp_j = len(self.list_of_branch) - 1
        if j == 0:
            self.list_of_branch.append(None)
            self.list_of_branch.append(None)
        else:
            if j < 2 * j + 2:
                while tmp_j != 2 * j + 2:
                    self.list_of_branch.append(None)
                    tmp_j += 1

        self.list_of_branch[2 * j + 2] = self.element(left_child, value_of_low_band, None, None, 2 * j + 2)
        a = self.ABC(self.list_of_branch[2 * j + 2].lower_bound, 2 * j + 2)
        self.list_of_low_bound.append(a)
        ###############################################################################################################
        ###### Powtórzenie korku 3
        ###############################################################################################################
        # Dodanie lewego wyciętego
        # Wycięcie i zablokowanie drogi powrotnej

        tmp_tab1 = copy.copy(left_child)
        left_child_2 = zeros((len(tmp_tab1) - 1, len(tmp_tab1) - 1), int)
        prv_x = tuple_max_in_min[1]
        l = 0
        tmp_xx = tmp_tab1[0, :].tolist()
        try:
            pxx = tmp_xx.index(tuple_max_in_min[1])

            tmp_yy = tmp_tab1[:, 0].tolist()
            try:
                pyy = tmp_yy.index(tuple_max_in_min[2])
                tmp_tab1[pxx, pyy] = -1
            except:
                pass
        except:
            pass
        for i in range(len(tmp_tab1)):
            c = 0
            for z in range(len(tmp_tab1)):
                if i != pyy:
                    if z != pxx:
                        left_child_2[l][c] = tmp_tab1[i][z]

                if z == pxx:
                    c -= 1
                c += 1

            if i == pyy:
                l -= 1
            l += 1

        value_of_low_band -= tuple_max_in_min[0]

        # Blokowanie m,p
        blok_x = self.list_of_branch[j][2]
        blok_y = tuple_max_in_min[2]

        tmp_xx = left_child_2[0, :].tolist()
        try:
            blok_y = tmp_xx.index(blok_y)

            tmp_yy = left_child_2[:, 0].tolist()
            try:
                blok_x = tmp_yy.index(blok_x)
            except:
                pass
        except:
            pass

        left_child_2[blok_x][blok_y] = -1
        # redukcja wierszy i kolumn
        count_row = len(left_child_2) - 1

        list_of_min_in_row = self.find_min_in_row(left_child_2, count_row)
        left_child_2 = self.sub_min_in_row(left_child_2, count_row, list_of_min_in_row)

        list_of_min_in_column = self.find_min_in_column(left_child_2, count_row)
        left_child_2 = self.sub_min_in_column(left_child_2, count_row, list_of_min_in_column)

        value_of_low_band += self.low_bound(list_of_min_in_row, list_of_min_in_column, count_row)

        self.list_of_branch[2 * j + 1] = self.element(left_child_2, value_of_low_band, tuple_max_in_min[1],
                                                      tuple_max_in_min[2], 2 * j + 1)

        a = self.ABC(self.list_of_branch[2 * j + 1].lower_bound, 2 * j + 1)
        self.list_of_low_bound.append(a)



    # def add_elements(self, tab,value_of_low_band, x, y,prv_x, indeks):
    #
    #     tmp_tab = copy.copy(tab)
    #
    #
    #     # 0 - lewe dziecko wycięte , 1 - prawe zaznaczone
    #     # children = self.add_children_and_cut(tmp_tab, x, y, indeks)
    #     tmp_xx = tab[0, 1:].tolist()
    #     try:
    #         yy = tmp_xx.index(y) + 1
    #         tmp_yy = tab[1:, 0].tolist()
    #         try:
    #             prv_x = tmp_yy.index(prv_x) + 1
    #
    #         except:
    #             pass
    #     except:
    #         pass
    #
    #     #   LEWY
    #
    #     if tab[prv_x][yy] == 0:
    #         a = self.min_without(tab[1:, yy], prv_x)
    #         b = self.min_without(tab[prv_x , 1:], yy - 1)
    #         if a == "False" or b == "False":
    #             pass
    #         else:
    #             value_of_low_band += a + b  # kolumna potem wiersz
    #
    #             tmp_tab[prv_x][yy] = - 1
    #
    #     children = self.add_children_and_cut(tmp_tab, x, y, indeks)
    #
    #
    #     # tmp_tab = copy.copy(children[0])
    #     # #0 - value, 1 - x, 2 - y
    #     # list_of_min_in_row = self.find_min_in_row(tmp_tab,len(children[0]) - 1)
    #     # if list_of_min_in_row != True:
    #     #     tmp_tab = self.sub_min_in_row(tmp_tab, len(children[0]) - 1, list_of_min_in_row)            # odjęcie wierszy
    #     #
    #     #     list_of_min_in_column = self.find_min_in_column(tmp_tab,len(children[0]) - 1)
    #     #     if list_of_min_in_column != True:
    #     #         tmp_tab = self.sub_min_in_column(tmp_tab,len(children[0]) - 1,list_of_min_in_column)        # odjęcie kolumn
    #     #
    #     #         value_of_low_band1 = self.low_bound(list_of_min_in_row,list_of_min_in_column,len(children[0]) - 1) + value_of_low_band     #trzeba dodać do poprzedniej
    #     #
    #     #         # 0 - value, 1 - x ,2 - y
    #     #         tuple_max_in_min =  self.find_max_opty(tmp_tab)
    #
    #
    #     left = self.element(children[0], value_of_low_band, None, None,2*indeks+1)
    #     #     else:
    #     #         left = True
    #     # else:
    #     #     left = True
    #
    #
    #     #   PRAWY
    #     tmp_tab = copy.copy(children[1])
    #
    #     # list_of_min_in_row = self.find_min_in_row(tmp_tab, len(children[1]) - 1)
    #     # if list_of_min_in_row != True:
    #     #     tmp_tab = self.sub_min_in_row(tmp_tab, len(children[1]) - 1, list_of_min_in_row)  # odjęcie wierszy
    #     #
    #     #     list_of_min_in_column = self.find_min_in_column(tmp_tab, len(children[1]) - 1)
    #     #     if list_of_min_in_column != True:
    #     #         tmp_tab = self.sub_min_in_column(tmp_tab, len(children[1]) - 1, list_of_min_in_column)  # odjęcie kolumn
    #
    #
    #
    #     # value_of_low_band2 = self.low_bound(list_of_min_in_row, list_of_min_in_column,len(children[1]) - 1)  + value_of_low_band # trzeba dodać do poprzedniej
    #
    #     # 0 - value, 1 - x ,2 - y
    #     tuple_max_in_min = self.find_max_opty(tab)
    #     try:
    #         value_of_low_band2 = value_of_low_band + tuple_max_in_min[0] - a - b
    #     except:
    #         value_of_low_band2 = value_of_low_band + tuple_max_in_min[0]
    #     right = self.element(tmp_tab, value_of_low_band2, None, None, 2*indeks+2)
    #
    #
    #
    #
    #     # print("Dzieci\n",children)
    #     # print("Lewy\n",left)
    #     # print("Prawy\n",right)
    #
    #     return left , right

    def add_element1(self,tab,value_of_low_band ,indeks):
        if len(tab) != 3:
            ###############################################################################################################
            # Krok 2
            ###############################################################################################################

            # Szukanie max kosztu wyłączenia
            # 0 - value, 1 - x ,2 - y
            tuple_max_in_min = self.find_max_opty(tab)

            #   Dodanie prawego dziecka z zablokowana droga o max opt kosztem wylaczenia

            value_of_low_band += tuple_max_in_min[0]

            tmp_xx = tab[0, :].tolist()
            # zablokowanie
            try:
                px = tmp_xx.index(tuple_max_in_min[2])
                tmp_yy = tab[:, 0].tolist()
                try:
                    py = tmp_yy.index(tuple_max_in_min[1])
                    tab[px, py] = -1
                    # tab[pyy, pxx] = -1
                except:
                    pass
            except:
                pass

            # powiększenie drzewa
            tmp_j = len(self.list_of_branch) - 1
            if indeks == 0:
                self.list_of_branch.append(None)
                self.list_of_branch.append(None)
            else:
                if tmp_j < 2 * indeks + 2:
                    while tmp_j != 2 * indeks + 2:
                        self.list_of_branch.append(None)
                        tmp_j += 1

            self.list_of_branch[2 * indeks + 2] = self.element(tab, value_of_low_band, None, None, 2 * indeks + 2)
            a = self.ABC(self.list_of_branch[2 * indeks + 2].lower_bound, 2 * indeks + 2)
            self.list_of_low_bound.append(a)
            ###############################################################################################################
            # Krok 3
            ###############################################################################################################


            # Dodanie lewego wyciętego
            # Wycięcie i zablokowanie drogi powrotnej

            tmp_tab1 = copy.copy(tab)
            left_child = zeros((len(tab) - 1, len(tab) - 1), int)

            l = 0
            tmp_xx = tmp_tab1[0, :].tolist()
            try:
                pxx = tmp_xx.index(tuple_max_in_min[1])

                tmp_yy = tmp_tab1[:, 0].tolist()
                try:
                    pyy = tmp_yy.index(tuple_max_in_min[2])
                    tmp_tab1[pxx, pyy] = -1
                except:
                    pass
            except:
                pass
            for i in range(len(tmp_tab1)):
                c = 0
                for z in range(len(tmp_tab1)):
                    if i != pyy:
                        if z != pxx:
                            left_child[l][c] = tmp_tab1[i][z]

                    if z == pxx:
                        c -= 1
                    c += 1

                if i == pyy:
                    l -= 1
                l += 1

            value_of_low_band -= tuple_max_in_min[0]

            # redukcja wierszy i kolumn
            count_row = len(left_child) - 1

            list_of_min_in_row = self.find_min_in_row(left_child, count_row)
            left_child = self.sub_min_in_row(left_child, count_row, list_of_min_in_row)

            list_of_min_in_column = self.find_min_in_column(left_child, count_row)
            left_child = self.sub_min_in_column(left_child, count_row, list_of_min_in_column)

            value_of_low_band += self.low_bound(list_of_min_in_row, list_of_min_in_column, count_row)

            self.list_of_branch[2 * indeks + 1] = self.element(left_child, value_of_low_band, tuple_max_in_min[1],
                                                          tuple_max_in_min[2], 2 * indeks + 1)

            ###############################################################################################################
            # Krok 4
            ###############################################################################################################
            ##### Powtórzenie korku 2
            ###############################################################################################################
            j = 2 * indeks + 1
            # Szukanie max kosztu wyłączenia
            # 0 - value, 1 - x ,2 - y
            tuple_max_in_min = self.find_max_opty(left_child)

            #   Dodanie prawego dziecka z zablokowana droga o max opt kosztem wylaczenia
            if tuple_max_in_min[0] != "False":
                value_of_low_band += tuple_max_in_min[0]
            else:
                value_of_low_band1 = None


            tmp_xx = left_child[0, :].tolist()
            # zablokowanie
            try:
                px = tmp_xx.index(tuple_max_in_min[1])
                tmp_yy = left_child[:, 0].tolist()
                try:
                    py = tmp_yy.index(tuple_max_in_min[2])
                    left_child[py, px] = -1
                    # tab[pyy, pxx] = -1
                except:
                    pass
            except:
                pass

            # powiększenie drzewa
            tmp_j = len(self.list_of_branch) - 1
            if j == 0:
                self.list_of_branch.append(None)
                self.list_of_branch.append(None)
            else:
                if tmp_j < 2 * j + 2:
                    while tmp_j != 2 * j + 2:
                        self.list_of_branch.append(None)
                        tmp_j += 1

            # self.list_of_branch[2 * j + 2] = self.element(left_child, value_of_low_band, None, None, 2 * j + 2)
            # a = self.ABC(self.list_of_branch[2 * j + 2].lower_bound, 2 * j + 2)
            # self.list_of_low_bound.append(a)

            if tuple_max_in_min[0] != "False":
                self.list_of_branch[2 * j + 2] = self.element(tab, value_of_low_band, None, None, 2 * j + 2)
                #a = self.ABC(self.list_of_branch[2 * j + 2].lower_bound, 2 * j + 2)
            else:
                self.list_of_branch[2 * j + 2] = self.element(tab, value_of_low_band1, None, None, 2 * j + 2)
            ###############################################################################################################
            ###### Powtórzenie korku 3
            ###############################################################################################################
            # Dodanie lewego wyciętego
            # Wycięcie i zablokowanie drogi powrotnej

            tmp_tab1 = copy.copy(left_child)
            left_child_2 = zeros((len(tmp_tab1) - 1, len(tmp_tab1) - 1), int)

            l = 0
            tmp_xx = tmp_tab1[0, :].tolist()
            try:
                pxx = tmp_xx.index(tuple_max_in_min[2])

                tmp_yy = tmp_tab1[:, 0].tolist()
                try:
                    pyy = tmp_yy.index(tuple_max_in_min[1])
                    tmp_tab1[pxx, pyy] = -1
                except:
                    pass
            except:
                pass
            for i in range(len(tmp_tab1)):
                c = 0
                for z in range(len(tmp_tab1)):
                    if i != py:
                        if z != px:
                            left_child_2[l][c] = tmp_tab1[i][z]

                    if z == px:
                        c -= 1
                    c += 1

                if i == py:
                    l -= 1
                l += 1

            value_of_low_band -= tuple_max_in_min[0]

            # Blokowanie m,p
            blok_x = self.list_of_branch[j][2]
            blok_y = tuple_max_in_min[2]

            tmp_xx = left_child_2[0, :].tolist()
            try:
                blok_y = tmp_xx.index(blok_y)

                tmp_yy = left_child_2[:, 0].tolist()
                try:
                    blok_x = tmp_yy.index(blok_x)
                    left_child_2[blok_x][blok_y] = -1
                except:
                    pass
            except:
                pass


            # redukcja wierszy i kolumn
            count_row = len(left_child_2) - 1

            list_of_min_in_row = self.find_min_in_row(left_child_2, count_row)
            left_child_2 = self.sub_min_in_row(left_child_2, count_row, list_of_min_in_row)

            list_of_min_in_column = self.find_min_in_column(left_child_2, count_row)
            left_child_2 = self.sub_min_in_column(left_child_2, count_row, list_of_min_in_column)

            value_of_low_band += self.low_bound(list_of_min_in_row, list_of_min_in_column, count_row)

            self.list_of_branch[2 * j + 1] = self.element(left_child_2, value_of_low_band, tuple_max_in_min[1],
                                                          tuple_max_in_min[2], 2 * j + 1)

            a = self.ABC(self.list_of_branch[2 * j + 1].lower_bound, 2 * j + 1)
            self.list_of_low_bound.append(a)

        else:
        ##############################################################################################################
        # Krok 5
        ###############################################################################################################
        ###### Powtórzenie kroku 2
        ###############################################################################################################
            # Szukanie max kosztu wyłączenia
            # 0 - value, 1 - x ,2 - y
            tuple_max_in_min = self.find_max_opty(tab)

            #   Dodanie prawego dziecka z zablokowana droga o max opt kosztem wylaczenia

            if tuple_max_in_min[0] != "False":
                value_of_low_band += tuple_max_in_min[0]
            else:
                value_of_low_band1 = None

            tmp_xx = tab[0, :].tolist()
            # zablokowanie
            try:
                px = tmp_xx.index(tuple_max_in_min[1])
                tmp_yy = tab[:, 0].tolist()
                try:
                    py = tmp_yy.index(tuple_max_in_min[2])
                    tab[py, px] = -1
                    # tab[pyy, pxx] = -1
                except:
                    pass
            except:
                pass

            # powiększenie drzewa
            tmp_j = len(self.list_of_branch) - 1
            if indeks == 0:
                self.list_of_branch.append(None)
                self.list_of_branch.append(None)
            else:
                if tmp_j < 2 * indeks + 2:
                    while tmp_j != 2 * indeks + 2:
                        self.list_of_branch.append(None)
                        tmp_j += 1
            if tuple_max_in_min[0] != "False":
                self.list_of_branch[2 * indeks + 2] = self.element(tab, value_of_low_band, None, None, 2 * indeks + 2)
                a = self.ABC(self.list_of_branch[2 * indeks + 2].lower_bound, 2 * indeks + 2)
            else:
                self.list_of_branch[2 * indeks + 2] = self.element(tab, value_of_low_band1, None, None, 2 * indeks + 2)

            a = self.ABC(self.list_of_branch[2 * indeks + 2].lower_bound, 2 * indeks + 2)
            self.list_of_low_bound.append(a)
            # Dodanie lewego wyciętego
            # Wycięcie i zablokowanie drogi powrotnej

            tmp_tab1 = copy.copy(tab)
            left_child = zeros((len(tab) - 1, len(tab) - 1), int)

            l = 0
            tmp_xx = tmp_tab1[0, :].tolist()
            try:
                pxx = tmp_xx.index(tuple_max_in_min[1])

                tmp_yy = tmp_tab1[:, 0].tolist()
                try:
                    pyy = tmp_yy.index(tuple_max_in_min[2])
                    tmp_tab1[pxx, pyy] = -1
                except:
                    pass
            except:
                pass
            for i in range(len(tmp_tab1)):
                c = 0
                for z in range(len(tmp_tab1)):
                    if i != pyy:
                        if z != pxx:
                            left_child[l][c] = tmp_tab1[i][z]

                    if z == pxx:
                        c -= 1
                    c += 1

                if i == pyy:
                    l -= 1
                l += 1

            self.list_of_branch[2 * indeks + 1] = self.element(left_child, value_of_low_band, tuple_max_in_min[1],
                                                              tuple_max_in_min[2], 2 * indeks + 1)

            a = self.ABC(self.list_of_branch[2 * indeks + 1].lower_bound, 2 * indeks + 1)
            self.list_of_low_bound.append(a)


    def find_min_in_row(self,tab,count_row):
        list_of_min_in_row = []
        # Przeszukanie wierszy w celu szukania minimum### oraz odfiltrowanie 0
        flag = False
        for i in range(count_row ):
            try:
                a = (min(filter(lambda x: x >= 0, tab[i + 1, 1:])))
            except ValueError:
                flag = True
            if flag == False:
                tmp_array = tab[i + 1, 1:].tolist()
                id = tab[0][tmp_array.index(a)]
                y = tab[i][0]
                p = self.my_struct(a, id, y)
                list_of_min_in_row.append(p)
            else:
                return True
        return list_of_min_in_row

    def sub_min_in_row(self,tab,count_row,list_of_min_in_row):
        # odejmowanie w wierszach
        for i in range(count_row):
            for j in range(count_row):
                if tab[i + 1][j + 1] > 0:

                    tab[i + 1][j + 1] = tab[i + 1][j + 1] - list_of_min_in_row[i][0]
        return tab

    def find_min_in_column(self,tab,count_row):
        list_of_min_in_column = []
        flag = False
        # Przeszukanie kolumn w celu szukania minimum oraz odfiltrowanie 0
        for i in range(count_row):
            try:
                a = (min(filter(lambda x: x >= 0, tab[1:, i + 1])))
            except ValueError:
                flag = True
            if flag == False:
                tmp_array = tab[1:, i + 1].tolist()
                id = tab[tmp_array.index(a)][0]
                x = tab[0][i]
                p = self.my_struct(a, x, id)
                list_of_min_in_column.append(p)
            else:
                return True
        return list_of_min_in_column

    def sub_min_in_column(self, tab, count_row, list_of_min_in_column):
        # odejmowanie w kolumnach
        for i in range(count_row):
            for j in range(count_row):
                if tab[j + 1][i + 1] > 0:
                    tab[j + 1 ][i + 1] = tab[j + 1][i + 1] - list_of_min_in_column[i].value
        return tab

    # Przy obliczaniu low band dla macierzy antysymetrycznej trzeba uwzględnić jeszcze pioneowe minima wg pkt b
    def low_bound(self,list_of_min_in_row,list_of_min_in_colum,count_row):
        value_of_low_band = 0

        for i in range(count_row):
            value_of_low_band += list_of_min_in_row[i].value + list_of_min_in_colum[i].value

        #print('\nValue of low bound: ', value_of_low_band)
        return value_of_low_band

    def find_max_opty(self, tab):

        Opt_cost_for_evry_zero = []

        for i in range(len(tab) - 1):
           for j in range(len(tab) - 1):
               if tab [i + 1][j + 1] == 0:
                   #vr = (min(filter(lambda x: x >= 0, tab[:, [i]])) + (min(filter(lambda x: x >= 0, tab[j, :]))))#[i,;]
                   a = self.min_without(tab[1:, j + 1],i)
                   b = self.min_without(tab[i + 1, 1:],j)
                   if a == "False" or b == "False":
                       x = tab[0][j + 1]
                       y = tab[i + 1][0]
                       vr = "False"   # kolumna potem wiersz
                       er = self.my_struct(vr, x,y)
                       Opt_cost_for_evry_zero.append(er)
                   else:
                       vr = a + b   # kolumna potem wiersz
                       x = tab[0][j+  1]
                       y = tab[i + 1][0]
                       er = self.my_struct(vr,x,y)
                       Opt_cost_for_evry_zero.append(er)

        flag = False
        for i in range(len(Opt_cost_for_evry_zero)):
            if Opt_cost_for_evry_zero[i][0] != "False":
                flag = True

        if flag == True:
            maxii = - 2
            for i in range(len(Opt_cost_for_evry_zero)):
                if Opt_cost_for_evry_zero[i][0] != "False":
                    if Opt_cost_for_evry_zero[i][0] > maxii:
                        maxii = Opt_cost_for_evry_zero[i][0]
                        maxi = Opt_cost_for_evry_zero[i]

        else:
            maxi = max(Opt_cost_for_evry_zero)




        #print("\nROW: ",Opt_cost_for_evry_zero,"\nMaxi: ",maxi)

        # 0 - value, 1 - x, 2 - y
        return  maxi[0], maxi[1], maxi[2]

    def add_children_and_cut(self,tab,tmp_x, tmp_y,indeks):

        tmp_xx = tab[0, 1:].tolist()
        px = tmp_xx.index(tmp_x) + 1
        tmp_yy = tab[1: , 0].tolist()
        py = tmp_yy.index(tmp_y) + 1


        # Powiększenie tablicy jeśli kolejne dziecko będzie poza zakresem tablicy
        #print(len(self.list_of_branch))
        k = indeks
        tmp_k = len(self.list_of_branch) -1
        if k == 0:
            self.list_of_branch.append(None)
            self.list_of_branch.append(None)
        else:
            if k < 2*k + 2:
                while tmp_k != 2*k + 2:
                    self.list_of_branch.append(None)
                    tmp_k += 1




        # Dodanie elementu dla prawego potomka
        # self.list_of_branch[2*k +2] = tmp_tab
        tmp_tab_right = copy.copy(tab)

        tmp_tab_right[py,px] = -1



        # Dodanie elementu dla lewego potomka
        #self.list_of_branch[2*k +1] = None


        # mechanizm wycinania gałęzi( kolumna i wiersz)
        tmp_tab_left = zeros((len(tab) -1,len(tab)-1),int)
        # print(tmp_tab)
        j = 0

        tmp_xx = tab[0, 1:].tolist()
        try:
            pxx = tmp_xx.index(tmp_y) + 1
            tmp_yy = tab[1:, 0].tolist()
            try:
                pyy = tmp_yy.index(tmp_x) + 1
                tmp_value = tab[pyy, pxx]
                tab[pyy, pxx] = -1
            except:
                pass
        except:
            pass

        for i  in range(len(tab)):
            c = 0
            for z in range(len(tab)):
                if i != py :
                    if z != px:

                        tmp_tab_left[j][c] = tab[i][z]

                if z == px:
                    c -= 1
                c += 1

            if i == py:
                j -= 1
            j += 1
        # to jest głupie ale działa ... póki co
        # if tmp_tab_left[len(tmp_tab_left)-1][len(tmp_tab_left)-1] == -1 :
        #     tmp_tab_left[len(tmp_tab_left)-1][len(tmp_tab_left)-1] = tmp_value

        return tmp_tab_left , tmp_tab_right

    def min_without(self, tab, without):
        min = max(tab)

        flag = "False"
        for i in range(len(tab)):
            if tab[i] <= min and i != without and tab[i] >= 0:
                min = tab[i]
                flag = "True"
        if flag == "False":
            return "False"
        else:
            return min

    def display(self, tab):
        print('\n',tab)

    def display_list(self,list):
        print('\n')
        for i in range(len(list)):
            print('Value: %ld   <%i,%s>' %(list[i][0],list[i][1],list[i][2]))
















 # def find_max_in_min(self,tab,list_of_min_in_row,list_of_min_in_colum):
    #     tmp_max = -1
    #     tmp_x = 0
    #     tmp_y = 0
    #
    #     for i in range(len(tab[:, 1])):
    #         if tmp_max < list_of_min_in_row[i][0]:
    #             tmp_max = list_of_min_in_row[i][0]
    #             tmp_x = list_of_min_in_row[i][1]
    #             tmp_y = list_of_min_in_row[i][2]
    #
    #         if tmp_max < list_of_min_in_colum[i][0]:
    #             tmp_max = list_of_min_in_colum[i][0]
    #             tmp_x = list_of_min_in_colum[i][1]
    #             tmp_y = list_of_min_in_colum[i][2]
    #
    #     # self.display_list(list_of_min_in_row)
    #     # self.display_list(list_of_min_in_colum)
    #     # print("\nMaksymalny element w minimach: ", tmp_max, "o indeksach:<", tmp_x, ",", tmp_y, ">")
    #
    #
    #     # to narazie nie potrzebne
    #     # cost_x = min(filter(lambda x: x > 0, tab[tmp_y, :]))
    #     # cost_y = min(filter(lambda x: x > 0, tab[:, tmp_x]))
    #
    #     # print("\nNajmniejszy element w kolumnie ", tmp_x, " wynosi: ", cost_x, "\nNajmniejszy element w wierszu ",
    #     #       tmp_y, " wynosi: ", cost_y)
    #
    #     return tmp_max, tmp_x, tmp_y


            # def my_min(self, tab):
            #
            #     # if tab[0] < 0:
            #     #     min = tab[1]
            #     # else:
            #     #     min = tab[0]
            #
            #     min = max(tab)
            #
            #     flag = False
            #     for i in tab:
            #         if i > 0 and min > i:
            #             min = i
            #         if flag == True and min > i and i >= 0:
            #             min = i
            #         if i == 0:
            #             flag = True
            #
            #     # print("\nMoje minimum: ", min)
            #     return min





    # funkcja szukająca dodatniego minimum większego od zera, chyba że w danym wierszu lub kolumnie zero występi więcej
    # niż raz

    #
    #
    #
    # def find_min_in_row_and_column(self):
    #
    #     list_of_min_in_row = []
    #     list_of_min_in_column = []
    #
    #
    #     for i in range(self.count_row):
    #         list_of_min_in_row.append(self.my_min(self.tab[i, :]))
    #
    #     for i in range(self.count_row):
    #         list_of_min_in_column.append(self.my_min(self.tab[:, i]))
    #
    #     max_row = max(list_of_min_in_row)
    #     max_column = max(list_of_min_in_column)
    #     my_max = max(max_row,max_column)
    #
    #     k = 0
    #     if max_row == my_max:
    #         index_row = list_of_min_in_row.index(my_max)
    #         print("\nIndeks w wierszu: ", index_row)
    #         k = 1
    #     else:
    #         index_column = list_of_min_in_column.index(my_max)
    #         print("\nIndeks w kolumnie: ", index_column)
    #         k = 2
    #
    #     print("\nMax: ", my_max)
    #     print("\nLista nowych minimów\nWiersze: ", list_of_min_in_row, "\nKolumny: ",list_of_min_in_column)


   # a = len(tab)
        # x = int(a/26)
        # r = a%26
        #
        # # Wyswietlenie pierwszego wiersza z etykietami
        # print("   ", end="")
        # for j in range(26*x + r):
        #     if j < 26:
        #         print(chr(65 + j)," ",end="")
        #     else:
        #         tmp_x = x + 1
        #         tmp_j = j -26
        #         while(tmp_x != 0):
        #             print(chr(65 + tmp_j),end="")
        #             tmp_x -= 1
        #         print(" ",end="")
        #
        # print('\n')