import random
import numpy as np
from util import *



def delta_exchange(solution: np.array, indices: list, nouvelles_valeurs: list) -> float:
    """
    Calcule le delta de coût (variation de distance) engendré par le remplacement
    des points situés aux positions `indices` dans `solution` par `nouvelles_valeurs`.

    Seules les distances impliquant des points modifiés et leurs voisins sont recalculées.

    Args:
        solution (np.ndarray): La solution actuelle (chemin).
        indices (list[int]): Liste triée des indices des points modifiés.
        nouvelles_valeurs (np.ndarray): Valeurs correspondant aux points à insérer.

    Returns:
        float: Variation de distance (nouvelle - ancienne).
    """
    n = len(solution)

    # Création d’un dictionnaire qui associe chaque index à sa nouvelle valeur
    echanges = {idx: val for idx, val in zip(indices, nouvelles_valeurs)}

    # Ensemble des arêtes affectées par la modification (voisins gauche/droite de chaque point modifié)
    edges = set()
    for idx in indices:
        if idx > 0:
            edges.add((idx - 1, idx))  # arête gauche
        if idx < n - 1:
            edges.add((idx, idx + 1))  # arête droite

    delta = 0.0

    # Pour chaque arête affectée, on compare l’ancienne distance et la nouvelle
    for a, b in edges:
        # Récupération des points initiaux
        old_a = solution[a]
        old_b = solution[b]
        old_cost = distance(old_a, old_b)

        # Substitution éventuelle par une nouvelle valeur si l’indice est modifié
        new_a = echanges.get(a, old_a)
        new_b = echanges.get(b, old_b)
        new_cost = distance(new_a, new_b)

        # Calcul du delta pour cette arête
        delta += new_cost - old_cost

    return delta




def echanger_points(solution: np.array, nbr_points: int, distance_actuelle: float) -> tuple:
    """
    Permute aléatoirement 'nbr_points' points et calcule le delta via delta_permutation.
    """
    if nbr_points < 2:
        return solution.copy(), distance_actuelle, False

    # Sélection aléatoire d'indices (hors du point fixe 0)
    indices = random.sample(range(1, len(solution) - 1), nbr_points)
    points_originaux = solution[indices].copy()
    points_melanges = points_originaux.copy()
    
    # Générer une permutation non triviale
    while True:
        np.random.shuffle(points_melanges)
        if not np.array_equal(points_melanges, points_originaux):
            break

    # Calcul du delta via la fonction factorisée
    delta = delta_exchange(solution, indices, points_melanges)

    if delta < 0:
        nouvelle_solution = solution.copy()
        nouvelle_solution[indices] = points_melanges
        return nouvelle_solution, distance_actuelle + delta, True
    else:
        return solution.copy(), distance_actuelle, False



# ---------------------------
# 3. Définition de l'échange de segments
# ---------------------------
def delta_exchange_segment(solution, debut, fin, nouveau_segment):
    """
    Calcule le delta de coût engfinré par le remplacement du segment 
    solution[debut:fin] par nouveau_segment.

    
    Args:
        solution (list ou np.array): Séquence de points.
        debut (int): Indice de début du segment à remplacer.
        fin (int): Indice de fin du segment à remplacer (non inclus).
        nouveau_segment (list): Nouveau segment de points de taille identique (ou compatible).
        
    Returns:
        float: Delta (coût nouveau - coût ancien) du remplacement.
    """
    n = len(solution)
    ancien_cout = 0.0
    nouveau_cout = 0.0

    # Ancien coût : raccords et arêtes internes
    if debut > 0:
        ancien_cout += distance(solution[debut - 1], solution[debut])
    for i in range(debut, fin - 1):
        ancien_cout += distance(solution[i], solution[i + 1])
    if fin < n:
        ancien_cout += distance(solution[fin - 1], solution[fin])

    # Nouveau coût : raccords et arêtes internes
    if debut > 0:
        nouveau_cout += distance(solution[debut - 1], nouveau_segment[0])
    for i in range(len(nouveau_segment) - 1):
        nouveau_cout += distance(nouveau_segment[i], nouveau_segment[i + 1])
    if fin < n:
        nouveau_cout += distance(nouveau_segment[-1], solution[fin])

    return nouveau_cout - ancien_cout

precedent = None  

def echanger_segment_consecutif(solution: np.array, nbr_points: int, distance_actuelle: float) -> tuple:
    """Effectue une selection de `nbr_points` consécutif choisis aléatoirement dans la solution, mélange cette selection de points
    et réinjecte la selection mélangée dans la solution de base si la solution est bénéfique sinon renvoie un flag montrant que la modification n'était pas bénéfique

    Args:
        solution (np.array): solution sur laquelle on veut opérer
        nbr_points (int): nombre de points pour la sélection 
        distance_actuelle (float): la distance de la solution actuelle 

    Returns:
        tuple: (nouvelle_solution, nouvelle_distance, modifié)
    """    
    global precedent
    n = len(solution)
    
    # Calcul des indices pour un segment de taille exacte 'nbr_points'
    max_start = n - nbr_points - 1  -1  # -1 pour end < n (car solution[end] doit exister)
    if max_start < 1:
        return solution.copy(), distance_actuelle, False
    
    # Choix aléatoire du début du segment en évitant 'precedent'
    debut = random.randint(1, max_start)
    while debut == precedent:
        debut = random.randint(1, max_start)
    precedent = debut
    
    fin = debut + nbr_points

    # Extraction et mélange du segment
    copie_solution = solution.copy()
    segment = copie_solution[debut:fin]
    original = segment.copy()
    
    # Mélanger jusqu'à obtenir un arrangement différent
    while True:
        np.random.shuffle(segment)
        if not np.array_equal(segment, original):
            break

    # Calcul du delta
    delta = delta_exchange_segment(solution, debut, fin, segment)

    if delta < 0:
        copie_solution[debut:fin] = segment
        return copie_solution, distance_actuelle + delta, True
    else:
        return solution.copy(), distance_actuelle, False

# ---------------------------
# 3. Définition du 2opt
# ---------------------------
def delta_2opt(solution: np.array, i: int, j: int) -> float:
    """
    Calcule le delta de coût engfinré par une inversion 2-opt sur le segment [i, j].

    
    Args:
        solution (list ou np.array): Séquence de points.
        i (int): Indice de début de l'inversion (i >= 1).
        j (int): Indice de fin de l'inversion (j < len(solution)-1).
        
    Returns:
        float: Le delta calculé (coût nouveau - coût ancien).
    """
    n = len(solution)
    
    A = solution[i - 1]
    B = solution[i]
    C = solution[j]

    #La solution est cyclique (pour gérer le retour à l'origine), ce qui implique que solution[(j+1) % n] correspond à l'élément suivant.
    D = solution[(j + 1) % n]
    
    ancien_cout = distance(A, B) + distance(C, D)
    nouveau_cout = distance(A, C) + distance(B, D)
    
    return nouveau_cout - ancien_cout

def deux_opt(solution: np.ndarray, recuit: bool = False, distance_actuelle: float = None):
    """
    Tire deux indices de manière aléatoire dans la solution et inverse l'ordre des points entre ces deux indices.
    
    En mode non recuit (recuit == False), l'inversion n'est effectuée que si l'opération améliore la solution 
    (delta négatif). La fonction renvoie alors (solution_modifiée, nouvelle_distance, True) ou (solution, distance_actuelle, False).
    
    En mode recuit (recuit == True), l'inversion est toujours appliquée et une copie modifiée de la solution est renvoyée.
    
    Args:
        solution (np.ndarray): La solution sur laquelle opérer.
        recuit (bool): Si True, on renvoie une solution modifiée dans tous les cas, sinon on n'accepte la modification que si 
                       elle est profitable.
        distance_actuelle (float): La distance totale courante (nécessaire en mode non recuit). 
                                  Si None, elle sera calculée via distance_totale(solution).
    
    Returns:
        - Si recuit == False : tuple (solution_modifiée, nouvelle_distance, bool: modification_effectuée)
        - Si recuit == True  : np.ndarray (solution modifiée)
    """
    # Conserver une copie pour éviter de modifier la solution d'origine
    new_solution = solution.copy()
    n = len(new_solution)
    
    # Pour préserver les points fixes (par ex. (0,0) au début et à la fin), on tire dans l'intervalle [1, n-1)
    # (si vous souhaitez aussi fixer le dernier point, vous pouvez tirer dans range(1, n-1))
    i, j = sorted(random.sample(range(1, n - 1), 2))
    
    # Calcul du delta pour l'inversion du segment [i, j] à l'aide de delta_2opt (à définir séparément)
    if not recuit:
        delta = delta_2opt(new_solution, i, j)
        # Si distance_actuelle n'est pas fourni, on le calcule
        if distance_actuelle is None:
            distance_actuelle = distance_totale(new_solution)
        # En mode optimisation, on n'accepte que l'inversion si elle améliore la solution (delta < 0)
        if delta < 0:
            new_solution[i:j+1] = new_solution[i:j+1][::-1]
            new_distance = distance_actuelle + delta
            return new_solution, new_distance, True
        else:
            return new_solution, distance_actuelle, False
    else:
        # Mode recuit : on effectue systématiquement l'inversion, et on renvoie la nouvelle solution (copie modifiée)
        new_solution[i:j+1] = new_solution[i:j+1][::-1]
        return new_solution

        
    

