from util import *
from common import *
import random

def voisin(S,nb_voisin_ech=1):
    #nb_voisin_ech déterminer au hasard
    nb_voisin_ech = random.randint(2,6)
    Sprime = echanger_segment_consecutif(S,nb_voisin_ech)

    # affiche_tournee(Sprime)
    return Sprime

def temperature(t,fonction):
    if fonction(t)<0:
        print("-------------------------------------------------")
    return fonction(t)

def prob(dE,T):
    if dE<0:
        return 1
    else:
        return np.exp(-dE/(T+0.00001))

fonction1 = lambda x:A*alpha**x
fonction2 = lambda x:1.8*(1-x/1)
fonction1 = lambda x:1.8 - 1.8*np.cos()
fonction3 = lambda x: 1.8/np.log(1 + x)

def recruit_simule(S0,kmax=10,nb_arc_ech=1,fonction=fonction3):
    S=S0
    meilleur_dist = float('inf')
    for k in range(1,kmax):
        print(k)
        Sprime = voisin(S,nb_arc_ech)
        if prob(distance_totale(Sprime)-distance_totale(S),temperature(k/kmax,fonction))>=random.uniform(0,1):
            print(k)
            S=Sprime
    return S

coord = lire_fichier_coords("exemple2.txt")
#affiche_points(coord)
#affiche_tournee(S)
A = 0.5
alpha = 0.99



# new_S = recruit_simule(S,30000,1,fonction=fonction2)
# affiche_tournee(S)
# affiche_tournee(new_S)