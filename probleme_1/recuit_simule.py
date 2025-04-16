from util import *
import random
from glouton import *


def voisin(S,nb_voisin_ech=1):
    #nb_voisin_ech déterminer au hasard
    Sprime = echanger_segment_consecutif(S,nb_voisin_ech)

    # affiche_tournee(Sprime)
    return Sprime

def temperature(t,fonction):
    return fonction(t)

def prob(dE,T):
    if dE<0:
        return 1
    else:
        return np.exp(-dE/T)

def recruit_simule(S0,kmax=10,nb_arc_ech=1,fonction=None):
    S=S0
    for k in range(1,kmax):
        print(k)
        Sprime = voisin(S,nb_arc_ech)
        if prob(distance_totale(S)-distance_totale(Sprime),temperature(k/kmax,fonction))>=random.uniform(0,1):
            print(k)
            S=Sprime
    return S

coord = lire_fichier_coords("exemple2.txt")
affiche_points(coord)

S = glouton(coord)
#affiche_tournee(S)
A = 100
alpha = 0.95
new_S = recruit_simule(S,1000,1,fonction= lambda x:A*alpha**x)
affiche_tournee(S)
affiche_tournee(new_S)