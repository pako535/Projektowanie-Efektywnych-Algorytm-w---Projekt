import macierz
import komiwojazer



tab = macierz.creatematrix_ATSP()
komi = komiwojazer.Komiwojazer(tab)
komi.display()
komi.low_bound()
print('\n')
komi.display()
#komi.find_max_in_row_and_column()
komi.find_max_and_cut()




