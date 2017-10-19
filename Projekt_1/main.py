import macierz
import komiwojazer

macierz.creatematrix()

tab = macierz.creatematrix()
komi = komiwojazer.Komiwojazer(tab)
komi.display()
komi.low_bound()
print('\n')
komi.display()
komi.find_min_in_row_and_column()




