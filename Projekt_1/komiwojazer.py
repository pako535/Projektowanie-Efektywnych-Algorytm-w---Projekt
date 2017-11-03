import macierz
from collections import namedtuple
from numpy import*
import copy

#   Brak usuwania odpowiednich kolumn i wierszy
#
#





# Wykorzystuje metode Litte'a (1962) dla algorytmu podziału i ograniczeń
class Komiwojazer:


    def __init__(self , tab):

        self.indeks = 0
        self.my_struct = namedtuple("my_struct",['value','x','y'])
        self.tab = tab
        # self.count_row = len(self.tab[:, 1])
        # self.list_of_min_in_row = []
        # self.value_of_low_band = 0
        # self.list_of_min_in_colum = []


        self.element = namedtuple("element", ['tab', 'bound', 'del_x', 'del_y','index'])
        element = self.add_element(tab)
        self.list_of_branch = [element]

        #print(self.list_of_branch)
        # element = self.element(tab,self.low_bound_init(tab),None,None,0)
        # self.list_of_branch[0] = element
        #
        # print(self.list_of_branch,sep="\n",end="")

    def my_main(self):
        tmp_indeks = self.indeks

        children = self.add_elements(self.list_of_branch[0].tab,self.list_of_branch[0].bound,
                                     self.list_of_branch[0].del_x,self.list_of_branch[0].del_y,self.indeks)

        self.list_of_branch[2*tmp_indeks + 1] = children [0]
        self.list_of_branch[2*tmp_indeks + 2] = children [1]

        # print(*self.list_of_branch, sep='\n\n')

        tmp_indeks = self.indeks

        # print("BOUND: ",self.list_of_branch[1].bound)
        children = self.add_elements(self.list_of_branch[1].tab, self.list_of_branch[1].bound,
                                     self.list_of_branch[1].del_x, self.list_of_branch[1].del_y, 1)


        # print(len(self.list_of_branch))
        self.list_of_branch[2 * 1 + 1] = children[0]
        self.list_of_branch[2 * 1 + 2] = children[1]

        print(*self.list_of_branch, sep='\n\n')

    def add_element(self,tab):
        #my_struct = namedtuple("my_struct", ['value', 'x', 'y'])
        count_row = len(tab[:, 1])

        tmp_tab = copy.copy(tab)
        list_of_min_in_row = self.find_min_in_row(tmp_tab, count_row)
        tmp_tab = self.sub_min_in_row(tmp_tab, count_row, list_of_min_in_row)
        list_of_min_in_column = self.find_min_in_column(tmp_tab, count_row)
        tmp_tab = self.sub_min_in_column(tmp_tab, count_row, list_of_min_in_column)

        # 0 - value, 1 - x ,2 - y
        tuple_max_in_min = self.find_max_in_min(tmp_tab, list_of_min_in_row, list_of_min_in_column)

        value_of_low_band = self.low_bound(list_of_min_in_row, list_of_min_in_column, count_row)

        element = self.element(tmp_tab,value_of_low_band,tuple_max_in_min[1], tuple_max_in_min[2],0)


        return element


    def add_elements(self, tab,value_of_low_band, x, y, indeks):

        tmp_tab = copy.copy(tab)

        #print(value_of_low_band)

        # 0 - lewe dziecko wycięte , 1 - prawe zaznaczone
        children = self.add_children_and_cut(tmp_tab, x, y, indeks)

        print("LEWE DZIECKO: ",children[0])
        #   LEWY
        # coś tu nie gra
        tmp_tab = copy.copy(children[0])

        list_of_min_in_row = self.find_min_in_row(tmp_tab,len(children[0]))
        tmp_tab = self.sub_min_in_row(tmp_tab, len(children[0]), list_of_min_in_row)            # odjęcie wierszy

        list_of_min_in_column = self.find_min_in_column(tmp_tab,len(children[0]))
        tmp_tab = self.sub_min_in_column(tmp_tab,len(children[0]),list_of_min_in_column)        # odjęcie kolumn
        print ("ROW: ",list_of_min_in_row,"\nCOLUMN: ",list_of_min_in_column)
        value_of_low_band += self.low_bound(list_of_min_in_row,list_of_min_in_column,len(children[0]))       #trzeba dodać do poprzedniej

        # 0 - value, 1 - x ,2 - y
        tuple_max_in_min = self.find_max_in_min(tmp_tab,list_of_min_in_row,list_of_min_in_column)
        self.indeks += 1

        left = self.element(children[0], value_of_low_band, tuple_max_in_min[1], tuple_max_in_min[2], self.indeks)



        #   PRAWY
        tmp_tab = copy.copy(children[1])

        list_of_min_in_row = self.find_min_in_row(tmp_tab, len(children[1]))
        tmp_tab = self.sub_min_in_row(tmp_tab, len(children[1]), list_of_min_in_row)  # odjęcie wierszy

        list_of_min_in_column = self.find_min_in_column(tmp_tab, len(children[1]))
        tmp_tab = self.sub_min_in_column(tmp_tab, len(children[1]), list_of_min_in_column)  # odjęcie kolumn

        value_of_low_band += self.low_bound(list_of_min_in_row, list_of_min_in_column,len(children[1]))  # trzeba dodać do poprzedniej

        # 0 - value, 1 - x ,2 - y
        tuple_max_in_min = self.find_max_in_min(tmp_tab, list_of_min_in_row, list_of_min_in_column)
        self.indeks += 1

        right = self.element(children[1], value_of_low_band, tuple_max_in_min[1], tuple_max_in_min[2], self.indeks)





        # print("Dzieci\n",children)
        # print("Lewy\n",left)
        # print("Prawy\n",right)

        return left , right

    def find_min_in_row(self,tab,count_row):
        list_of_min_in_row = []
        # Przeszukanie wierszy w celu szukania minimum### oraz odfiltrowanie 0
        for i in range(count_row):
            try:
                a = (min(filter(lambda x: x >= 0, tab[i, :])))
            except ValueError:
                a = 0
            tmp_array = tab[i, :].tolist()
            id = tmp_array.index(a)
            p = self.my_struct(a, id, i)
            list_of_min_in_row.append(p)

        return list_of_min_in_row

    def sub_min_in_row(self,tab,count_row,list_of_min_in_row):
        # odejmowanie w wierszach
        for i in range(count_row):
            for j in range(count_row):
                if tab[i][j] > 0:
                    tab[i][j] = tab[i][j] - list_of_min_in_row[i][0]
        return tab

    def find_min_in_column(self,tab,count_row):
        list_of_min_in_column = []

        # Przeszukanie kolumn w celu szukania minimum oraz odfiltrowanie 0
        for i in range(count_row):
            try:
                a = (min(filter(lambda x: x >= 0, tab[:, i])))
            except ValueError:
                a = 0
            tmp_array = tab[:, i].tolist()
            id = tmp_array.index(a)
            p = self.my_struct(a, i, id)
            list_of_min_in_column.append(p)

        return list_of_min_in_column

    def sub_min_in_column(self, tab, count_row, list_of_min_in_column):
        # odejmowanie w kolumnach
        for i in range(count_row):
            for j in range(count_row):
                if tab[j][i] > 0:
                    tab[j][i] = tab[j][i] - list_of_min_in_column[i].value
        return tab

    # Przy obliczaniu low band dla macierzy antysymetrycznej trzeba uwzględnić jeszcze pioneowe minima wg pkt b
    def low_bound(self,list_of_min_in_row,list_of_min_in_colum,count_row):
        value_of_low_band = 0

        for i in range(count_row):
            value_of_low_band += list_of_min_in_row[i].value + list_of_min_in_colum[i].value

        #print('\nValue of low bound: ', value_of_low_band)
        return value_of_low_band

    def find_max_in_min(self,tab,list_of_min_in_row,list_of_min_in_colum):
        tmp_max = -1
        tmp_x = 0
        tmp_y = 0

        for i in range(len(tab[:, 1])):
            if tmp_max < list_of_min_in_row[i][0]:
                tmp_max = list_of_min_in_row[i][0]
                tmp_x = list_of_min_in_row[i][1]
                tmp_y = list_of_min_in_row[i][2]

            if tmp_max < list_of_min_in_colum[i][0]:
                tmp_max = list_of_min_in_colum[i][0]
                tmp_x = list_of_min_in_colum[i][1]
                tmp_y = list_of_min_in_colum[i][2]

        # self.display_list(list_of_min_in_row)
        # self.display_list(list_of_min_in_colum)
        # print("\nMaksymalny element w minimach: ", tmp_max, "o indeksach:<", tmp_x, ",", tmp_y, ">")


        # to narazie nie potrzebne
        # cost_x = min(filter(lambda x: x > 0, tab[tmp_y, :]))
        # cost_y = min(filter(lambda x: x > 0, tab[:, tmp_x]))

        # print("\nNajmniejszy element w kolumnie ", tmp_x, " wynosi: ", cost_x, "\nNajmniejszy element w wierszu ",
        #       tmp_y, " wynosi: ", cost_y)

        return tmp_max,tmp_x,tmp_y

    def add_children_and_cut(self,tab,tmp_x, tmp_y,indeks):

        # Powiększenie tablicy jeśli kolejne dziecko będzie poza zakresem tablicy
        #print(len(self.list_of_branch))
        k = indeks
        tmp_k = indeks
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
        tmp_tab_right[tmp_y,tmp_x] = -1



        # Dodanie elementu dla lewego potomka
        #self.list_of_branch[2*k +1] = None


        # mechanizm wycinania gałęzi( kolumna i wiersz)
        tmp_tab_left = zeros((len(tab) -1,len(tab)-1),int)
        # print(tmp_tab)
        j = 0
        tab [tmp_x ,tmp_y] = -1
        for i  in range(len(tab)):
            c = 0
            for z in range(len(tab)):
                if i != tmp_y :
                    if c != tmp_x:
                        tmp_tab_left[j][c] = tab[i][z]

                if z == tmp_x:
                    c -= 1
                c += 1

            if i == tmp_y:
                j -= 1
            j += 1

        return tmp_tab_left , tmp_tab_right

    def display(self, tab):
        print('\n',tab)

    def display_list(self,list):
        print('\n')
        for i in range(len(list)):
            print('Value: %ld   <%i,%s>' %(list[i][0],list[i][1],list[i][2]))





































    # funkcja szukająca dodatniego minimum większego od zera, chyba że w danym wierszu lub kolumnie zero występi więcej
    # niż raz

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
    #              flag = True
    #
    #     #print("\nMoje minimum: ", min)
    #     return min
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
