import random
import numpy as np

def echanger_points(solution: np.array, nbr_points: int) -> list:
    # On prend k indices aléatoire, les indices des (0,0) exclus
    indices = random.sample(range(1, len(solution) - 1), nbr_points)
    indices.sort()

    # On récupère les points associés aux indices
    sous_segment = solution[indices].copy()
    
    # On mélange ces points
    original = sous_segment.copy() 
    while True :
        np.random.shuffle(sous_segment)
        if not np.array_equal(sous_segment, original):
                break
    nouvelle = solution.copy()

    # On remplace par les points mélangés aux indices des points de base 
    nouvelle[indices] = sous_segment
    return nouvelle


precedent = None  
def echanger_segment_consecutif(solution: np.array, nbr_points: int) -> list:
    # on stock l'indice précédentn afin d'éviter les redondances 
    # ? est ce que c'est vraiment un gain au final en complexité 
    global precedent
    indice = random.randint(1, len(solution) - 2) # on ne veut pas echanger (0,0)

    if indice != precedent:
        precedent = indice

        # On ne veut pas shuffle (0,0) donc on adapte les indices de début et de fin 
        debut = max(indice - nbr_points // 2 , 1)
        fin = min(indice + nbr_points // 2 + 1, len(solution) - 1)
        copie_solution = solution.copy()
        valeurs_segment = copie_solution[debut:fin]
        original = valeurs_segment.copy()
        while True:
            np.random.shuffle(valeurs_segment)
            if not np.array_equal(valeurs_segment, original):
                break
        np.random.shuffle(valeurs_segment)
        copie_solution[debut:fin] = valeurs_segment
        return copie_solution
    return solution


#liste_test = np.array([(5,5),(3,0),(2,4),(8,9),(2,2)])

#print(echanger_points(liste_test,3))
#print(echanger_segment_consecutif(liste_test,4))
