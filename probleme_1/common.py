import random
import numpy as np

def echanger_points(solution: np.array, nbr_points: int) -> list:
    """Prendre une selection de 'nbr_points points' de manière aléatoire , les mélange entre eux puis les remets dans la solution

    Args:
        solution (np.array): solution sur laquelle on veut opérer
        nbr_points (int):  nombre de points pour la sélection 

    Returns:
        list: copie de la solution avec les points échangés
    """    
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
    """Effectue une selection de `nbr_points` consécutif choisis aléatoirement dans la solution, mélange cette selection de points
    et réinjecte la selection mélangée dans la solution de base

    Args:
        solution (np.array): solution sur laquelle on veut opérer
        nbr_points (int): nombre de points pour la sélection 

    Returns:
        list: copie de la solution avec les points échangés
    """    
    # on stock l'indice précédent afin d'éviter les redondances 
    global precedent
    indice = random.randint(1, len(solution) - 2) # on ne veut pas echanger (0,0)

    while indice == precedent:
        indice = random.randint(1, len(solution) - 2) # on ne veut pas echanger (0,0)

    precedent = indice

    # On ne veut pas shuffle (0,0) donc on adapte les indices de début et de fin 
    debut = max(indice - nbr_points // 2 , 1)
    fin = min(indice + nbr_points // 2 + 1, len(solution) - 1)

    # On effectue une première copie de la solution
    copie_solution = solution.copy()

    # On récupère la sélection de points à mélanger
    valeurs_segment = copie_solution[debut:fin]

    # On garde la sélection original
    original = valeurs_segment.copy()

    
    while True:
        # On shuffle
        np.random.shuffle(valeurs_segment)
        # On s'assure que le mélange crée une sélection différente 
        if not np.array_equal(valeurs_segment, original):

            # Si c'est le cas on arrête de mélanger
            break
            
        # Sinon on remélange jusqu'à obtenir une solution différente

    np.random.shuffle(valeurs_segment)
    copie_solution[debut:fin] = valeurs_segment
    return copie_solution

def deux_opt(solution: np.ndarray) -> np.ndarray:
    """Tire deux indice dans la solution de manière aléatoire et inverse l'ordre des points entre ces deux indices

    Args:
        solution (np.ndarray): solution sur laquelle on va opérer

    Returns:
        np.ndarray: copie de la solution modifiée 
    """    
    n = len(solution)

    # Selection d'indices aleatoires dans la solution de base
    i, j = sorted(random.sample(range(1, n), 2))
    
    # Inversion du segment [i, j] dans une copie 
    nouvelle = np.concatenate((
        solution[:i],
        solution[i:j+1][::-1],
        solution[j+1:]
    ))
    
    return nouvelle

