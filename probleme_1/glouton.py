from util import *
from main import appel_cacul_tournee
import random
import numpy as np
import math
import copy 

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
    # On utilise une copie de la solution glouton pour éviter de modifier la solution d'origine
    solution_actuelle = solution_glouton[:]  
    amelioration_trouvee = True
    
    # Tant qu'une amélioration est détectée, on poursuit l'optimisation
    while amelioration_trouvee:
        amelioration_trouvee = False
        # Parcourir toutes les tailles de fenêtre entre k_min et k_max
        for k in range(k_min, k_max + 1):
            # Balayage de la solution avec une fenêtre de taille k
            for i in range(len(solution_actuelle) - k + 1):
                # Extraction de la sous-partie de la solution
                sous_partie = solution_actuelle[i : i + k]
                # Optimisation de la sous-partie via la fonction appel_cacul_tournee
                modification = appel_cacul_tournee(sous_partie)
                
                # Suppression du point de retour (0, 0) en fin et en début de la solution optimisée
                modification.pop()   # enlève le dernier élément
                modification.pop(0)  # enlève le premier élément
                
                # Construction de la solution candidate avec la sous-partie optimisée
                solution_candidate = solution_actuelle[:i] + modification + solution_actuelle[i + k:]
                
                # Si la solution candidate présente une distance totale inférieure, elle est retenue
                if distance_totale(solution_candidate) < distance_totale(solution_actuelle):
                    solution_actuelle = solution_candidate
                    amelioration_trouvee = True
                    # Dès qu'une amélioration est trouvée, on sort de la première boucle 
                    break
            
            # On sort de la deuxième boucle puis on recommence le processus sur notre nouvelle solution. 
            if amelioration_trouvee:
                break

    return solution_actuelle


# ---------------------------
# 3. Heuristique locale par échange de deux points 
# ---------------------------
points_precedents = (-1, -1)
def echanger_points(solution: list, nbr_points: int) -> list:
    # On prend k indices aléatoire, les indices des (0,0) exclus
    indices = random.sample(range(1, len(solution) - 1), nbr_points)
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


def heuristique_locale_echange(solution_glouton: list, nbr_points: int = 5, max_stagnation: int = 1000)-> list:
    nb_ameliorations = 0
    stagnation = 0
    solution_optimisee = solution_glouton
    while nb_ameliorations < max_stagnation and stagnation < max_stagnation:
        solution_potentielle = echanger_points(solution_optimisee, nbr_points)
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
def echanger_segment_consecutif(solution: list, nbr_points: int) -> list:
    # on stock l'indice précédentn afin d'éviter les redondances 
    # ? est ce que c'est vraiment un gain au final en complexité 
    global precedent
    indice = random.randint(1, len(solution) - 2) # on ne veut pas echanger (0,0)

    if indice != precedent:
        precedent = indice

        # On ne veut pas shuffle (0,0) donc on adapte les indices de début et de fin 
        debut = max(indice - nbr_points // 2, 1)
        fin = min(indice + nbr_points // 2 + 1, len(solution) - 1)
        copie_solution = solution[:]
        indices_segment = list(range(debut, fin))
        valeurs_segment = [copie_solution[j] for j in indices_segment]
        random.shuffle(valeurs_segment)
        for idx, val in zip(indices_segment, valeurs_segment):
            copie_solution[idx] = val
        return copie_solution
    return solution

def heuristique_locale_echange_segment(solution_glouton: list, nbr_points: int = 4, max_stagnation: int = 1000) -> list:
    nb_ameliorations = 0
    stagnation = 0
    solution_optimisee = solution_glouton

    # On continue d'essayer des amélioration jusqu'à ce qu'une des conditions soit remplie 
    while nb_ameliorations < max_stagnation and stagnation < max_stagnation:
        solution_potentielle = echanger_segment_consecutif(solution_optimisee, nbr_points)
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

# ordre fenetre , echange, echange segment 
heuristiques_locales = [heuristique_locale_echange, heuristique_locale_echange_segment, heuristique_locale_fenetre_dynamique]

# ---------------------------
# 6. Approche hybride combinant les approches 
# ---------------------------
def hybride(solution_initiale: list, heuristiques: list[callable], nb_iter_max: int = 100, stagnation_max: int = 100, delta_min: float = 0.001) -> list:
    solution_courante = solution_initiale
    nb_iterations = 0
    stagnation = 0
    cout_courant = distance_totale(solution_courante)
    
    while nb_iterations < nb_iter_max and stagnation < stagnation_max:
        amelioration = False
        for heuristique in heuristiques:
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

solution_amelioree = hybride(solution_initiale, heuristiques_locales)

print("Distance totale améliorée :", distance_totale(solution_amelioree))
