from util import *
from common import *
import random

def voisin(S):
    """Génère une nouvelle solution proche de S

    Args:
        S (): _description_

    Returns:
        _type_: _description_
    """
    nb_voisin_ech = random.randint(1,4)
    for i in range(0,nb_voisin_ech):
        Sprime = deux_opt(S)
    return Sprime

def temperature(t,fonction):
    """Applique la fonction temperature passée en argument à t

    Args:
        t (float): 
        fonction (function): fonction de la température

    Returns:
        float: la temperature à l'instant t
    """
    return fonction(t)

def prob(dE,T):
    if dE<0: #si dE<0 alors distance_totale(Sprime)<distance_totale(S)
        # donc Sprime et plus interessant que S -> On le choisit avec une probas de 1
        return 1
    else:
        return np.exp(-dE/(T+0.00001))  #+0.00001 : pour eviter d'avoir une erreur si T=0

#Test avec differentes fonctions de températures
fonction1 = lambda x:A*alpha**x
fonction2 = lambda x:1.8*(1-x/1)
fonction1 = lambda x:1.8 - 1.8*np.cos()
fonction3 = lambda x: 1.8/np.log(1 + x)

def recruit_simule(S0,kmax=10,fonction=fonction3):
    S=S0 
    for k in range(1,kmax):
        Sprime = voisin(S)  
        #la condition d'acceptation du Sprime comme nouveau S depend de la proba et du hasard
        if prob(distance_totale(Sprime)-distance_totale(S),temperature(k/kmax,fonction))>=random.uniform(0,1):
            S=Sprime
    return S

coord = lire_fichier_coords("exemple2.txt")
#affiche_points(coord)
#affiche_tournee(S)
A = 0.5
alpha = 0.99
