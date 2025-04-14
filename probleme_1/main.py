# Code de base pour le problème `Tournée du jardinier`

import util

def calcule_tournee(coords):
    return coords # A MODIFIER

coords = util.lire_fichier_coords('exemple1.txt')
tournee = calcule_tournee(coords)
<<<<<<< HEAD
#util.affiche_tournee(tournee)

#util.affiche_points(coords)
=======
util.affiche_tournee(tournee)

util.affiche_points(coords)
>>>>>>> e10cf29c8a00f4cc627235f9e9ce20135d1c12f5

distance_min = float("+inf")

def distance(p1, p2):
    return ( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )**(1/2)

def distance_totale(coords):
    if len(coords) == 0:
        return 0
    dist = distance((0, 0), coords[0]) + distance(coords[-1], (0, 0))
    for i in range(1, len(coords)):
        dist += distance(coords[i], coords[i-1])
    return dist

<<<<<<< HEAD
chemins = []

def calcul_tournee_ex(coords, curr=[],i=0):


    if len(coords) == 0:
        global chemins
=======
def calcul_tournee_ex(coords, curr=[]):
    
    chemins = []

    if len(coords) == 0:
>>>>>>> e10cf29c8a00f4cc627235f9e9ce20135d1c12f5
        chemins.append(curr[:])
        return min(chemins, key = util.distance_totale)

    for i in range(len(coords)):
        point = coords.pop(i)
        curr.append(point)

<<<<<<< HEAD
        result = calcul_tournee_ex(coords, curr,i+1)  # appel récursif

        curr.pop()
        coords.insert(i, point)  # on remet le point à sa place d'origine 
    return result

tournee = calcul_tournee_ex(list(coords))
print(tournee)
=======
        calcul_tournee_ex(coords, curr)  # appel récursif

        curr.pop()
        coords.insert(i, point)  # on remet le point à sa place d'origine 

    return min(chemins,key = util.distance_totale)

tournee = calcul_tournee_ex(list(coords))
>>>>>>> e10cf29c8a00f4cc627235f9e9ce20135d1c12f5
