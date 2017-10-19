import macierz
import komiwojazer

# macierz.creatematrix()

tab = macierz.creatematrix()
komi = komiwojazer.Komiwojazer(tab)
komi.display()
komi.low_bound()
print('\n')
komi.display()


