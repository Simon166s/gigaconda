from util import *
from main import appel_cacul_tournee
import random
import numpy as np
import math

# ---------------------------
# 1. Algorithme glouton pour générer la solution initiale
# ---------------------------
def glouton(coordonnees: np.array) -> list:
    # On commence à (0,0)
    point_courant = (0, 0)
    solution_courante = [point_courant]
    # On initialise les indices des coordonnées dans une liste pour savoir lesquels on à déjà visité
    non_visites = list(range(len(coordonnees)))
    while non_visites:
        # On trouve l'indice du point qui est associé à la plus petite distance du point courrant
        indice_min = min(non_visites, key=lambda i: distance(point_courant, coordonnees[i]))
        point_courant = tuple(coordonnees[indice_min])
        solution_courante.append(point_courant)
        non_visites.remove(indice_min)

    solution_courante.append((0, 0))
    return solution_courante

# ---------------------------
# 2. Heuristique locale avec fenêtre dynamique (k variant de k_min à k_max)
# ---------------------------
def heuristique_locale_fenetre_dynamique(solution_glouton: list, k_min: int = 3, k_max: int = 6) -> list:
    solution_optimisee = solution_glouton
    for k in range(k_min, k_max + 1):
        amelioration = False
        # Balayage de la solution par une fenêtre de taille k
        for i in range(len(solution_optimisee) - k + 1):
            sous_partie = solution_optimisee[i : i + k]
            # Appel à la fonction pour optimiser cette sous-partie
            changement = appel_cacul_tournee(sous_partie)

            # Suppression du point de retour (0, 0) s'il est présent
            if changement:
                if changement[-1] == (0, 0):
                    changement.pop()
                if changement and changement[0] == (0, 0):
                    changement.pop(0)
            
            solution_candidate = solution_optimisee[:i] + changement + solution_optimisee[i + k:]
            if distance_totale(solution_candidate) < distance_totale(solution_optimisee):
                solution_optimisee = solution_candidate
                amelioration = True
        # Si une amélioration a été trouvée pour ce k, on recommence à partir de k_min
        if amelioration:
            break
    return solution_optimisee

# ---------------------------
# 3. Heuristique locale par échange de deux points 
# ---------------------------
points_precedents = (-1, -1)
def echanger_points(solution: list, k: int = 4):
    # On prend k indices aléatoire, les indices des (0,0) exclus
    indices = random.sample(range(1, len(solution) - 1), k)
    indices.sort()

    # On récupère les points associés aux indices
    sous_segment = [solution[i] for i in indices]

    # On mélange ces points 
    random.shuffle(sous_segment)
    nouvelle = solution[:]

    # On remplace par les points mélangés aux indices des points de base 
    for i, idx in enumerate(indices):
        nouvelle[idx] = sous_segment[i]
    return nouvelle


def heuristique_locale_echange(solution_glouton: list, max_stagnation: int = 1000):
    nb_ameliorations = 0
    stagnation = 0
    solution_optimisee = solution_glouton
    while nb_ameliorations < max_stagnation and stagnation < max_stagnation:
        solution_potentielle = echanger_points(solution_optimisee)
        if distance_totale(solution_potentielle) < distance_totale(solution_optimisee):
            solution_optimisee = solution_potentielle
            nb_ameliorations += 1
        else:
            stagnation += 1

    return solution_optimisee

# ---------------------------
# 4. Heuristique locale par échange d'un segment de k points consécutifs
# ---------------------------
precedent = None  
def echanger_segment_consecutif(solution: list, k: int) -> list:
    # on stock l'indice précédentn afin d'éviter les redondances 
    # ? est ce que c'est vraiment un gain au final en complexité 
    global precedent
    indice = random.randint(1, len(solution) - 2) # on ne veut pas echanger (0,0)

    if indice != precedent:
        precedent = indice

        # On ne veut pas shuffle (0,0) donc on adapte les indices de début et de fin 
        debut = max(indice - k // 2, 1)
        fin = min(indice + k // 2 + 1, len(solution) - 1)
        copie_solution = solution[:]
        indices_segment = list(range(debut, fin))
        valeurs_segment = [copie_solution[j] for j in indices_segment]
        random.shuffle(valeurs_segment)
        for idx, val in zip(indices_segment, valeurs_segment):
            copie_solution[idx] = val
        return copie_solution
    return solution

def heuristique_locale_echange_segment(solution_glouton: list, k: int = 4, max_stagnation: int = 1000) -> list:
    nb_ameliorations = 0
    stagnation = 0
    solution_optimisee = solution_glouton

    # On continue d'essayer des amélioration jusqu'à ce qu'une des conditions soit remplie 
    while nb_ameliorations < max_stagnation and stagnation < max_stagnation:
        solution_potentielle = echanger_segment_consecutif(solution_optimisee, k)
        if distance_totale(solution_potentielle) < distance_totale(solution_optimisee):
            solution_optimisee = solution_potentielle
            nb_ameliorations += 1
            stagnation = 0
        else:
            stagnation += 1
    return solution_optimisee

# ---------------------------
# 5. Définition des voisinages pour la stratégie hybride
# ---------------------------


heuristiques_locales = [heuristique_locale_fenetre_dynamique, heuristique_locale_echange_segment, heuristique_locale_echange]

# ---------------------------
# 6. Approche hybride combinant les approches 
# ---------------------------
def hybride(solution_initiale: list, heuristiques: list[callable], nb_iter_max: int = 1000, stagnation_max: int = 1000, delta_min: float = 0.001) -> list:
    solution_courante = solution_initiale
    nb_iterations = 0
    stagnation = 0
    cout_courant = distance_totale(solution_courante)
    
    while nb_iterations < nb_iter_max and stagnation < stagnation_max:
        amelioration = False
        for heuristique in heuristiques_locales :
            solution_candidature = heuristique(solution_courante)
            cout_candidature = distance_totale(solution_candidature)

            # ? si l'amélioration n'est pas significative, on conserve la solution d'avant pour ne pas apporter du désordre 
            if cout_candidature < cout_courant * (1 - delta_min): 
                solution_courante = solution_candidature
                cout_courant = cout_candidature
                amelioration = True
                stagnation = 0  
                break  
        if not amelioration:
            stagnation += 1
        nb_iterations += 1
        
    return solution_courante

coordonnees = lire_fichier_coords("exemple2.txt")
solution_initiale = glouton(coordonnees)
print("Distance initiale :", distance_totale(solution_initiale))

solution_amelioree = hybride(solution_initiale, heuristiques_locales, nb_iter_max=1000, stagnation_max=100)
print("Distance totale améliorée :", distance_totale(solution_amelioree))
