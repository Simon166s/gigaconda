import random

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