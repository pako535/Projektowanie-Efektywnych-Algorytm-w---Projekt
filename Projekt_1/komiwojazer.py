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
        self.my_struct = namedtuple("my_struct",['value','x','y'])

        self.tab = tab
        # self.count_row = len(self.tab[:, 1])
        # self.list_of_min_in_row = []
        # self.value_of_low_band = 0
        # self.list_of_min_in_colum = []


        self.element = namedtuple("element", ['tab', 'bound', 'del_x', 'del_y','index'])
        self.list_of_branch = []
        element = self.element(tab,self.low_bound_init(tab),None,None,0)
        self.list_of_branch.append(element)



    # Przy obliczaniu low band dla macierzy antysymetrycznej trzeba uwzględnić jeszcze pioneowe minima wg pkt b
    def low_bound_init(self,tab):

        my_struct = namedtuple("my_struct", ['value', 'x', 'y'])
        count_row = len(tab[:, 1])
        list_of_min_in_row = []
        value_of_low_band = 0
        list_of_min_in_colum = []


        # #jesli lista minimów jest pełna to usuń by uzupełnić od nowa
        # if self.list_of_min_in_row:
        #     del self.list_of_min_in_row[ : ]
        # if self.list_of_min_in_colum :
        #     del self.list_of_min_in_colum[ : ]

        #Przeszukanie wierszy w celu szukania minimum### oraz odfiltrowanie 0
        for i in range(count_row):
            try:
                a = (min(filter(lambda x: x >= 0, tab[i, :])))
            except ValueError:
                a = 0
            tmp_array = tab[i, :].tolist()
            id = tmp_array.index(a)
            p = my_struct(a, id,i)
            list_of_min_in_row.append(p)


        #odejmowanie w wierszach
        for i in range(count_row):
            for j in range(count_row):
                if tab[i][j] > 0:
                    tab[i][j] = tab[i][j] - list_of_min_in_row[i][0]
            #print(self.list_of_min_in_row[i][0])

        # print("\n",self.list_of_min_in_row,'\n')
        # self.display()

        # Przeszukanie kolumn w celu szukania minimum oraz odfiltrowanie 0
        for i in range(count_row):
            a = (min(filter(lambda x: x >= 0, tab[:, i])))
            tmp_array = tab[:, i].tolist()
            id = tmp_array.index(a)
            p = my_struct(a, i, id)
            list_of_min_in_colum.append(p)



        # odejmowanie w kolumnach
        for i in range(count_row):
            for j in range(count_row):
                if tab[j][i] > 0:
                    tab[j][i] = tab[j][i] - list_of_min_in_colum[i].value

        # Sumowanie wartosci ograniczenia
        #self.value_of_low_band = sum(self.list_of_min_in_row[:][0]) + sum(self.list_of_min_in_colum[:][0])

        for i in range(count_row):
            value_of_low_band += list_of_min_in_row[i].value + list_of_min_in_colum[i].value


        print('\nValue of low bound: ', value_of_low_band)
        self.find_max_in_min_and_cut(tab,list_of_min_in_row,list_of_min_in_colum,0)
        return value_of_low_band



    def find_max_in_min_and_cut(self,tab,list_of_min_in_row, list_of_min_in_colum,init):


        tmp_max = -1
        tmp_x = 0
        tmp_y = 0
        cost_x = 0
        cost_y = 0


        for i in range(len(tab[:, 1])):
            if tmp_max < list_of_min_in_row[i][0]:
                tmp_max = list_of_min_in_row[i][0]
                tmp_x = list_of_min_in_row[i][1]
                tmp_y = list_of_min_in_row[i][2]

            if tmp_max < list_of_min_in_colum[i][0]:
                tmp_max = list_of_min_in_colum[i][0]
                tmp_x = list_of_min_in_colum[i][1]
                tmp_y = list_of_min_in_colum[i][2]



        self.display_list(list_of_min_in_row)
        self.display_list(list_of_min_in_colum)
        print("\nMaksymalny element w minimach: ", tmp_max, "o indeksach:<", tmp_x, ",", tmp_y, ">")
        # print(self.tab[tmp_y,:])
        cost_x = min(filter(lambda  x: x > 0,tab[tmp_y, :]))
        cost_y = min(filter(lambda  x: x > 0,tab[:, tmp_x]))

        print("\nNajmniejszy element w kolumnie ",tmp_x," wynosi: ",cost_x,"\nNajmniejszy element w wierszu ",tmp_y," wynosi: ",cost_y)

        #print(self.list_of_branch)


        # print(len(self.list_of_branch))
        # Powiększenie tablicy jeśli kolejne dziecko będzie poza zakresem tablicy
        # k = len(self.list_of_branch)
        # if k == 0:
        #     k = 1
        # if len(self.list_of_branch) < 2*(len(self.list_of_branch ) + 1):
        #     while len(self.list_of_branch) != 2*k + 1:
        #         self.list_of_branch.append(None)
        self.list_of_branch.append(None)
        self.list_of_branch.append(None)
        self.list_of_branch.append(None)
        k = len(self.list_of_branch)
        print(len(self.list_of_branch))


        # Dodanie elementu dla prawego potomka
        tmp_tab = copy.copy(tab)
        tmp_tab[tmp_y,tmp_x] = -1

        self.list_of_branch[2] = tmp_tab


        # Dodanie elementu dla lewego potomka
        #self.list_of_branch[2*k] = None


        tmp_tab = copy.copy(tab)
        tmp_tab = tmp_tab.tolist()
        tmp_tab = tmp_tab.remove(tmp_y)

        print(tab)
        print("asda\n",tmp_tab)
        self.list_of_branch[1] = None




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
