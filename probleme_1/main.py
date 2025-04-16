# Code de base pour le problème `Tournée du jardinier`
import matplotlib.pyplot as plt
from util import distance_totale, lire_fichier_coords, affiche_points, affiche_tournee,distance
import numpy as np

coords = lire_fichier_coords('exemple1.txt')

distance_min = float("+inf")

meilleur_chemins = np.array([])
taille_min_chem = float("+inf")


def calcul_tournee_ex(coords, curr = np.array([[0, 0]], dtype=float),long_actuel=0):
    global taille_min_chem, meilleur_chemins
    if taille_min_chem <= long_actuel:
        return
    
    if len(coords) == 0:
        
        d_tot = long_actuel+distance(curr[-1],[0,0])
        if d_tot < taille_min_chem:
            taille_min_chem = d_tot
            meilleur_chemins = np.vstack([curr, [0, 0]])
        return

    for i in range(len(coords)):
        point = coords[i]
        new_coords = np.delete(coords, i, axis=0)
        new_curr = np.vstack([curr, point])
        
        calcul_tournee_ex(new_coords, new_curr,long_actuel+distance(new_curr[-1],new_curr[-2]))


def appel_calcul_tournee(coords):
    global meilleur_chemins, taille_min_chem
    meilleur_chemins = np.empty((0, 2))
    taille_min_chem = float("+inf")
    
    # Convertir les coordonnées en numpy array si ce n'est pas déjà le cas
    coords_array = np.array(coords, dtype=float)
    
    calcul_tournee_ex(coords_array)
    return meilleur_chemins


tournee = appel_calcul_tournee(coords)
#print(tournee)

# affiche_points(coords)
# affiche_tournee(tournee)
