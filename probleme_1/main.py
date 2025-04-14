# Code de base pour le problème `Tournée du jardinier`
import matplotlib.pyplot as plt
from util import distance_totale, lire_fichier_coords, affiche_points, affiche_tournee

coords = lire_fichier_coords('test_alban_etoile.txt')

distance_min = float("+inf")

meilleur_chemins = []
taille_min_chem =  float("+inf")

def calcul_tournee_ex(coords, curr=[]):
    global taille_min_chem
    d_tot = distance_totale(curr)
    if taille_min_chem <= d_tot:
        return 
    if len(coords) == 0:
        global meilleur_chemins
        taille_min_chem = d_tot
        meilleur_chemins = curr[:]
        return 
    
    for i in range(len(coords)):
        point = coords.pop(i)
        curr.append(point)

        calcul_tournee_ex(coords, curr)  # appel récursif

        curr.pop()
        coords.insert(i, point)  # on remet le point à sa place d'origine

def appel_cacul_tournee(coords):
    global meilleur_chemins
    global taille_min_chem
    meilleur_chemins = []
    taille_min_chem =  float("+inf")
    calcul_tournee_ex(coords)
    return meilleur_chemins



tournee = appel_cacul_tournee(list(coords))
#print(tournee)

affiche_points(coords)
affiche_tournee(tournee)