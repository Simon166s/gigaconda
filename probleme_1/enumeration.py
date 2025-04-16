# Code de base pour le problème `Tournée du jardinier`
import matplotlib.pyplot as plt
from util import (
    distance_totale,
    lire_fichier_coords,
    affiche_points,
    affiche_tournee,
    distance,
)
import numpy as np
import math


coords = lire_fichier_coords("exemple1.txt")


def calcul_tournee_ex(
    coords: np.array,
    curr: np.array = np.array([[0, 0]], dtype=float),
    long_actuel: int = 0,
):
    """Trouve le chemin le plus court en utilisant la methode d'énumération exhaustive

    Args:
        coords (np.array): Coordonnées des points initiaux (coordonnées des arbres)
        curr (np.array, optional):  Defaults to np.array([[0, 0]], dtype=float).
        long_actuel (int, optional):  Defaults to 0.
    """
    global taille_min_chem, meilleur_chemins

    # verifie si la taille du chemin actuelle n'est pas superieure à la taille minimale, si oui on arrete de parcourir cette branche/chemin
    if taille_min_chem <= long_actuel:
        return

    # Partie Backtracking
    # Verifie que lorsqu'on a passé tt le points
    if len(coords) == 0:

        # On calcule la distance totale en ajoutant le parcours du dernier point au point de depart
        d_tot = long_actuel + distance(curr[-1], [0, 0])

        # On met a jour le chemin minimum si la distance est plus petite que taille_min_chemin
        if d_tot < taille_min_chem:

            taille_min_chem = d_tot
            meilleur_chemins = np.vstack([curr, [0, 0]])
        return

    # Enumeration Exhaustive
    for i in range(len(coords)):
        point = coords[i]
        new_coords = np.delete(coords, i, axis=0)
        new_curr = np.vstack([curr, point])

        calcul_tournee_ex(
            new_coords, new_curr, long_actuel + distance(new_curr[-1], new_curr[-2])
        )


def appel_enumeration_exhaustive(coords: np.array):
    """Appelle la fonction d'énumération exhaustive et utilise le backtracking pour simplifier le programme

    Args:
        coords (np.array): Coordonnées des points initiaux (coordonnées des arbres)

    Returns:
        meilleur_chemins (np.array): Chemin de plus courte passant par tt les points commencant par 0 et finissant par 0
    """
    # Initialisation des données
    global meilleur_chemins, taille_min_chem
    meilleur_chemins = np.empty((0, 2))
    taille_min_chem = float("+inf")

    calcul_tournee_ex(coords)
    return meilleur_chemins


if __name__ == "__main__":
    tournee = appel_enumeration_exhaustive(coords)
    print(tournee)

    affiche_points(coords)
    affiche_tournee(tournee)
