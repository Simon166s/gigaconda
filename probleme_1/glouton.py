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



previous_points = (-1, -1)
def echanger_arcs(solution):
    global previous_points
    i, j = random.sample(range(1, len(solution) - 1), 2)  # éviter le point de départ (0, 0)
    if (i,j) != previous_points:
        solution_copy = solution[:]
        solution_copy[i], solution_copy[j] = solution_copy[j], solution_copy[i]
        previous_points = (i,j)
        return solution_copy
    return solution


def local_heuristic_arc(solution_glouton: list, max_stagnation: int = 10000):
    sortir = False 
    nbr_meilleur = 0
    stagnation = 0
    current_better = solution_glouton
    while not sortir:

        potential_better_solution = echanger_arcs(current_better)
        if distance_totale(current_better) > distance_totale(potential_better_solution):
            current_better = potential_better_solution
            nbr_meilleur += 1
        else:
            stagnation += 1

        sortir = True if nbr_meilleur >= 100000 or stagnation >= max_stagnation else False 

    return current_better




previous = None  # à initialiser avant d'appeler la fonction

def echanger_arcs_k_consec(solution: list, k: int):
    global previous
    i = random.randint(1, len(solution) - 2)
    if i != previous:
        previous = i
        start = max(i - k // 2, 1)
        end = min(i + k // 2 + 1, len(solution) - 1)
        solution_copy = solution[:]
        slice_indices = range(start, end)
        slice_values = [solution_copy[j] for j in slice_indices]
        random.shuffle(slice_values)

        for idx, val in zip(slice_indices, slice_values):
            solution_copy[idx] = val

        return solution_copy
    return solution


def local_heuristic_arc_consec(solution: list, k: int, max_stagnation: int = 10000):
    sortir = False 
    nbr_meilleur = 0
    stagnation = 0
    current_better = solution
    while not sortir:

        potential_better_solution = echanger_arcs_k_consec(current_better, k)
        if distance_totale(current_better) > distance_totale(potential_better_solution):
            current_better = potential_better_solution
            nbr_meilleur += 1
        else:
            stagnation += 1

        sortir = True if nbr_meilleur >= 100000 or stagnation >= max_stagnation else False 

    return current_better




coords = lire_fichier_coords("exemple2.txt")
solution_init = glouton(coords)
print(distance_totale(solution_init))


local_heuristic_arc = local_heuristic_arc_consec(solution_init, 2)
print(distance_totale(local_heuristic_arc))

heuristic_k_pt = local_heuristic_k_pt(local_heuristic_arc, 6)
print(distance_totale(heuristic_k_pt))



# local_heuristic_arc = local_heuristic_arc(heuristic_k_pt)
# print(distance_totale(local_heuristic_arc))

