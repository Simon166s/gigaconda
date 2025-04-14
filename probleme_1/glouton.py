from util import *
from main import appel_cacul_tournee
import random


def glouton(coords: np.array):
    current_pt = (0, 0)
    current_solution = [current_pt]
    remaining = list(range(len(coords)))

    while remaining:
        idx_min = min(remaining, key=lambda i: distance(current_pt, coords[i]))
        current_pt = tuple(coords[idx_min])
        current_solution.append(current_pt)
        remaining.remove(idx_min)

    current_solution.append((0, 0))
    return current_solution


def local_heuristic_k_pt(solution_glouton: list, k: int):
    current_better = solution_glouton
    for i in range(
        len(current_better) - k + 1
    ):  # Déplacement de la fenêtre sur la tournée
        sub_part = current_better[
            i : i + k
        ]  # Extraction du segment de la fenêtre

        # Appel à la fonction pour optimiser cette sous-partie
        change = appel_cacul_tournee(sub_part)

        change.pop()  # Enlever le retour à (0, 0)
        change.pop(0)  # Enlever 

        solutionbis = current_better[:i] + change + current_better[i + k :]
        if distance_totale(solutionbis) < distance_totale(current_better):
            current_better = solutionbis

    return current_better

# De base j'ai fait ca mais sans volonté d'amélioration donc en fait ca revient a une fonction voisin 
# ? Plutot voisin que heuristique locale si on enleve la condition d'amelioration 

def echanger_arcs(solution):
    # Crée une copie de la solution avant de modifier
    solution_copy = solution[:]
    i, j = random.sample(range(1, len(solution_copy) - 1), 2)  # éviter le point de départ (0, 0)
    solution_copy[i], solution_copy[j] = solution_copy[j], solution_copy[i]
    return solution_copy


def local_heuristic_arc(solution_glouton: list, max_iter= 50):
    current_better = solution_glouton
    itr = 1
    while itr <= max_iter:
        potential_better_solution = echanger_arcs(current_better)
        current_better = (
            current_better
            if distance_totale(current_better)
            < distance_totale(potential_better_solution)
            else potential_better_solution
        )
        itr += 1 
    return current_better

# ? Idée echanger deux arcs jusqu'a ce que ce soit mieux ie prendre deux arcs et inverser leur point d'arriver ? 

coords = lire_fichier_coords("exemple2.txt")
solution_init = glouton(coords)
print(distance_totale(solution_init))

heuristic_k_pt = local_heuristic_k_pt(solution_init, 7)
print(distance_totale(heuristic_k_pt))

local_heuristic_arc = local_heuristic_arc(solution_init, 1000000)
print(distance_totale(local_heuristic_arc))

