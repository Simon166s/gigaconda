from util import *
from enumeration import appel_enumeration_exhaustive
from recuit_simule import recuit_simule
import numpy as np
from common import *


# ---------------------------
# 1. Algorithme glouton pour générer la solution initiale
# ---------------------------
def glouton(coordonnees: np.array) -> list:
    """Approche gloutonne qui fournit une solution basée une approche ou on prend a chaque fois le point
    le plus proche du point courant en terme de distance de manière à minimiser le parcours

    Args:
        coordonnees (np.array): array des coordonnés de chaque points du problème à résoudre

    Returns:
        list: la solution gloutonne générée
    """
    # On commence à (0,0)
    point_courant = (0, 0)
    solution_courante = [point_courant]
    # On initialise les indices des coordonnées dans une liste pour savoir lesquels on à déjà visité
    non_visites = list(range(len(coordonnees)))
    while non_visites:
        # On trouve l'indice du point qui est associé à la plus petite distance du point courrant
        indice_min = min(
            non_visites, key=lambda i: distance(point_courant, coordonnees[i])
        )
        point_courant = tuple(coordonnees[indice_min])
        solution_courante.append(point_courant)
        non_visites.remove(indice_min)

    solution_courante.append((0, 0))
    return np.array(solution_courante)


# ---------------------------
# 2. Heuristique locale avec fenêtre dynamique (k variant de k_min à k_max)
# ---------------------------
def heuristique_locale_fenetre_dynamique(
    solution_glouton: np.array, k_min: int = 3, k_max: int = 5
) -> list:
    """Optimise localement une solution en appliquant une heuristique de recherche par fenêtre dynamique.

    Cette fonction améliore la solution initiale obtenue par une approche gloutonne. Elle parcourt la solution à l'aide d'une fenêtre de taille variable (allant de k_min à k_max) et, pour chaque sous-séquence de points,
    elle applique un algorithme d'énumération exhaustive (via la fonction appel_enumeration_exhaustive) afin de trouver une permutation qui réduit la distance totale.
    Dès qu'une amélioration est détectée, la solution est mise à jour, et le processus est répété jusqu'à ce qu'aucune optimisation supplémentaire ne soit possible.

    Args:
        solution_glouton (np.array): la solution initiale
        k_min (int, optional): taille minimale de la fenêtre. Par défaut la valeur est 3.
        k_max (int, optional): taille maximale de la fenêtre. Par défaut la valeur est  6.

    Returns:
        list: La solution optimisée obtenue après avoir appliqué l'heuristique locale sur l'ensemble de la solution.
    """
    # On utilise une copie de la solution glouton pour éviter de modifier la solution d'origine
    solution_actuelle = solution_glouton.copy()
    amelioration_trouvee = True
    distance_actuelle = distance_totale(solution_glouton)
    # Tant qu'une amélioration est détectée, on poursuit l'optimisation
    while amelioration_trouvee:
        amelioration_trouvee = False
        # Parcourir toutes les tailles de fenêtre entre k_min et k_max
        for k in range(k_min, k_max + 1):
            # Balayage de la solution avec une fenêtre de taille k
            for i in range(len(solution_actuelle) - k + 1):
                sous_partie = solution_actuelle[i : i + k]
                modification = appel_enumeration_exhaustive(sous_partie)

                # Nettoyage des extrémités (évite les retour au début)
                modification = modification[1:-1]

                # Calcule du delta de coût sur la portion modifiée
                indices_modifies = list(range(i, i + len(modification)))
                delta = delta_exchange(
                    solution_actuelle, indices_modifies, modification
                )

                # Si on a une amélioration locale
                if delta < 0:
                    # Mise à jour partielle de la solution
                    for idx, val in zip(indices_modifies, modification):
                        solution_actuelle[idx] = val

                    distance_actuelle += delta
                    amelioration_trouvee = True
                    break  # sort de la boucle sur les fenêtres

            # On sort de la deuxième boucle puis on recommence le processus sur notre nouvelle solution.
            if amelioration_trouvee:
                break

    return solution_actuelle


# ---------------------------
# 3. Heuristique locale par échange de deux points
# ---------------------------


def heuristique_locale_echange(
    solution_glouton: np.array,
    nbr_points: int = 5,
    max_iter=10000,
    max_stagnation: int = 10000,
) -> np.array:
    """
    Optimise localement une solution en échangeant aléatoirement un certain nombre de points.

    Cette fonction applique une heuristique d'optimisation locale qui consiste à échanger des points
    dans la solution (obtenue par une approche gloutonne) pour tenter d’améliorer la distance
    totale parcourue. Pour chaque itération, un échange de `nbr_points` est réalisé via la fonction `echanger_points`.
    Si l'échange aboutit à une diminution de la distance totale, la solution est mise à jour et le compteur
    d'améliorations est incrémenté. Sinon, un compteur de stagnation est incrémenté. Le processus se poursuit
    jusqu'à atteindre le seuil maximum d'améliorations ou de stagnation.

    Args:
        solution_glouton (np.array): La solution initiale obtenue par une approche gloutonne, typiquement un tableau numpy représentant l’ordre des points.
        nbr_points (int, optional): Le nombre de points à échanger lors de chaque itération d'optimisation. Par défaut, la valeur est 5.
        max_stagnation (int, optional): Le nombre maximum d'itérations sans amélioration (ou nombre maximum d'améliorations) avant l'arrêt de l'optimisation. Par défaut, la valeur est 1000.

    Returns:
        np.array:
            La solution optimisée sous forme d'un tableau numpy après application de l'heuristique d'échange.
    """
    solution = (
        solution_glouton.copy()
    )  # Compteur pour suivre le nombre d'itérations sans amélioration
    stagnation = 0
    distance_actuelle = distance_totale(solution)
    compteur_iter = 0
    stagnation = 0

    while compteur_iter < max_iter and stagnation < max_stagnation:
        solution, distance_actuelle, modif = echanger_points(
            solution, nbr_points, distance_actuelle=distance_actuelle
        )
        if modif:
            stagnation = 0  # réinitialise car on a trouvé une amélioration
        else:
            stagnation += 1
        compteur_iter += 1
    return solution


# ---------------------------
# 4. Heuristique locale par échange d'un segment de k points consécutifs
# ---------------------------
def heuristique_locale_echange_segment(
    solution_glouton: np.array,
    nbr_points: int = 4,
    max_iter: int = 10000,
    max_stagnation: int = 10000,
) -> np.array:
    """
    Améliore localement une solution en échangeant des segments consécutifs de points.

    La fonction tente d'optimiser la solution initiale (obtenue par une méthode gloutonne)
    en réalisant des échanges de segments de `nbr_points` points de manière aléatoire. Si l'échange
    permet de réduire la distance totale (calculée par `distance_totale`), la solution est mise à jour.
    Le processus s'arrête dès qu'aucune amélioration n'est obtenue pendant `max_stagnation` itérations.

    Args:
        solution_glouton (np.array): La solution initiale sous forme de tableau numpy représentant l'ordre des points.
        nbr_points (int, optional): Le nombre de points consécutifs à échanger lors de chaque itération. Par défaut, la valeur est 4.
        max_stagnation (int, optional): Le nombre maximal d'itérations sans amélioration consécutive avant l'arrêt de l'algorithme. Par défaut, la valeur est 1000.

    Returns:
        np.array: La solution optimisée sous forme d'un tableau numpy.
    """
    solution = (
        solution_glouton.copy()
    )  # Compteur pour suivre le nombre d'itérations sans amélioration
    stagnation = 0
    distance_actuelle = distance_totale(solution)
    compteur_iter = 0
    stagnation = 0

    while compteur_iter < max_iter and stagnation < max_stagnation:
        solution, distance_actuelle, modif = echanger_segment_consecutif(
            solution, nbr_points, distance_actuelle=distance_actuelle
        )
        if modif:
            stagnation = 0  # réinitialise car on a trouvé une amélioration
        else:
            stagnation += 1
        compteur_iter += 1
    return solution


# 2-opt : échange de deux arêtes dans notre solution
def heuristique_locale_2_opt(solution_glouton, max_iter=100000, max_stagnation=100000):
    """
    Optimise localement une solution en appliquant l'algorithme 2-opt.

    Cette fonction met en œuvre l'heuristique 2-opt pour améliorer une solution initiale.
    À chaque itération, la fonction génère une solution candidate en échangeant deux segments de la solution actuelle. Si
    la distance totale de la solution candidate est inférieure, elle devient la nouvelle solution et le compteur de stagnation
    est réinitialisé. Sinon, le compteur de stagnation augmente. Le processus s'arrête lorsque le nombre d'itérations sans
    amélioration atteint max_stagnation.

    Args:
        solution_initiale (np.array): La solution initiale à optimiser, typiquement sous forme d'un tableau numpy représentant l'ordre des points.
        max_stagnation (int, optional): Le nombre maximal d'itérations sans amélioration avant d'arrêter l'algorithme. Par défaut, la valeur est 100000.

    Returns:
        np.array: La solution optimisée après application de l'algorithme 2-opt.
    """
    # Initialisation de la solution courante
    solution = (
        solution_glouton.copy()
    )  # Compteur pour suivre le nombre d'itérations sans amélioration
    stagnation = 0
    distance_actuelle = distance_totale(solution)
    compteur_iter = 0
    stagnation = 0

    while compteur_iter < max_iter and stagnation < max_stagnation:
        solution, distance_actuelle, modif = deux_opt(
            solution, recuit=False, distance_actuelle=distance_actuelle
        )
        if modif:
            stagnation = 0  # réinitialise car on a trouvé une amélioration
        else:
            stagnation += 1
        compteur_iter += 1
    return solution


# ---------------------------
# 5. Définition des voisinages pour la stratégie hybride
# ---------------------------

# ordre fenetre , echange, echange segment
heuristiques_locales = [
    heuristique_locale_echange_segment,  # grosses modifications
    heuristique_locale_echange,  # raffinage
    heuristique_locale_2_opt,  # bon polisseur général
    heuristique_locale_fenetre_dynamique,  # micro-optimisation variable
]


# ---------------------------
# 6. Approche hybride combinant les approches
# ---------------------------
def hybride(
    solution_initiale: np.array,
    heuristiques: list[callable] = heuristiques_locales,
    nb_iter_max: int = 10,
    stagnation_max: int = 10,
    delta_min: float = 0.001,
) -> np.array:
    """
    Combine plusieurs heuristiques pour optimiser une solution de manière hybride.

    Cette fonction applique successivement une liste d'heuristiques sur une solution initiale afin de la faire évoluer vers une meilleure solution.
    Lorsqu'une heuristique améliore suffisamment (définie par delta_min) la solution courante, celle-ci est adoptée et le compteur de stagnation est réinitialisé.
    L'algorithme s'arrête lorsque le nombre maximal d'itérations ou le nombre maximal d'itérations sans amélioration (stagnation) est atteint.

    Args:
        solution_initiale (np.array): La solution de départ à optimiser, typiquement représentée par un tableau numpy (par exemple, l'ordre des points dans un TSP).
        heuristiques (list[callable]): Une liste de fonctions heuristiques qui prennent une solution et renvoient une solution modifiée.
        nb_iter_max (int, optional): Le nombre maximal d'itérations de l'algorithme. Par défaut 100.
        stagnation_max (int, optional): Le nombre maximal d'itérations consécutives sans amélioration significative avant d'arrêter l'optimisation. Par défaut 100.
        delta_min (float, optional): Le pourcentage minimal d'amélioration requis sur le coût total (distance) pour considérer une solution comme améliorée. Par défaut 0.001.

    Returns:
        np.array: La solution optimisée sous forme de tableau numpy après application hybride des heuristiques.
    """
    # Initialisation de la solution courante, des compteurs et du coût de la solution
    solution_courante = solution_initiale
    nb_iterations = 0
    stagnation = 0
    cout_courant = distance_totale(solution_courante)

    # Boucle principale d'optimisation
    while nb_iterations < nb_iter_max and stagnation < stagnation_max:
        amelioration = False
        # Application des heuristiques une par une
        for heuristique in heuristiques:
            solution_candidature = heuristique(solution_courante)
            cout_candidature = distance_totale(solution_candidature)

            # Vérifie si la solution candidate présente une amélioration suffisante
            if cout_candidature < cout_courant * (1 - delta_min):
                # Mise à jour de la solution courante et réinitialisation du compteur de stagnation
                solution_courante = solution_candidature
                cout_courant = cout_candidature
                amelioration = True
                stagnation = 0
                break  # Arrête la boucle des heuristiques dès qu'une amélioration est trouvée

        # Si aucune heuristique n'a permis d'améliorer la solution, incrémente le compteur de stagnation
        if not amelioration:
            stagnation += 1

        nb_iterations += 1  # Incrémente le compteur global d'itérations

    return solution_courante


if __name__ == "__main__":
    coordonnees = lire_fichier_coords("exemple2.txt")
    solution_initiale = glouton(coordonnees)
    print("Distance initiale :", distance_totale(solution_initiale))

    # * Ajout du recuit
    solution_recuit = recuit_simule(solution_initiale)
    print("Distance recuit améliorée :", distance_totale(solution_recuit))

    solution_amelioree = hybride(solution_recuit, heuristiques_locales)
    print("Distance hybride améliorée :", distance_totale(solution_amelioree))
