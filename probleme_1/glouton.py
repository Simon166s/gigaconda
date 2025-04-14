from util import *
from main import calcul_tournee_ex

def glouton(coords: list):
    current_solution  = []
    current = (0,0)
    current_solution.append(current)
    while coords:
        coords.remove(current)
        current = min(coords, key= lambda p:  distance(current, p))
        current_solution.append(current)
        
    current_solution.append((0,0))
    return current_solution, distance_totale(current_solution)


def local_heuristic_4pt(solution_glouton: list):
    current_better = solution_glouton
    # for i in range(len(solution_glouton)):
    #     if i % 3 == 0:
    i = solution_glouton[len(solution_glouton) // 2]
    calcul_tournee_ex(solution_glouton[i: min(i + 4, len(solution_glouton))]) 
    solutionbis = solution_glouton[:i] + calcul_tournee_ex + solution_glouton[min(i+5, len(solution_glouton)):]
    if distance_totale(solutionbis) < distance_totale(current_better):
        current_better  = solutionbis  

        
print(glouton(lire_fichier_coords("exemple1.txt")))
