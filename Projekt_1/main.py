import macierz
import komiwojazer






tab = macierz.creatematrix_ATSP()
komi = komiwojazer.Komiwojazer(tab)
komi.my_main()
#komi.display(tab)
#komi.low_bound(tab)
# komi.find_min_in_row_and_column()

#komi.find_max_in_row_and_column()
#komi.find_max_in_min_and_cut()




