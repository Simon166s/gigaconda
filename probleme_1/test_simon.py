import main
import affichage
import util
import itertools

coords = util.lire_fichier_coords("exemple1.txt")
coords2 = util.lire_fichier_coords("exemple2.txt")

# util.affiche_points(coords)
# tournee = main.calcul_tournee_ex(list(coords))
# util.affiche_tournee(tournee)

# util.affiche_points(coords2)
# tournee2= main.calcul_tournee_ex(list(coords2))
# util.affiche_tournee(tournee2)

meilleure_tournee = min(itertools.permutations(coords), key=util.distance_totale)
util.affiche_tournee(meilleure_tournee)
