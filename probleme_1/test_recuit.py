from glouton import *
from recuit_simule import *


coord = lire_fichier_coords("exemple2.txt")

fonction2 = lambda x:2.5*(1-x/1)

heuristiques_locales = [heuristique_locale_2_opt]
solution_initiale = glouton(coord)
solution_amelioree = heuristique_locale_2_opt(solution_initiale)

new_S = recruit_simule(solution_amelioree,30000,fonction=fonction2)
affiche_tournee(solution_amelioree)
affiche_tournee(new_S)