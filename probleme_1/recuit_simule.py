from util import *
from common import *
import random


def voisin(S):
    """Génère une nouvelle solution proche de S

    Args:
        S (numpy a): Solution provisoire

    Returns:
        Sprime solution voisine de S
    """
    nb_voisin_ech = random.randint(1, 4)
    for i in range(0, nb_voisin_ech):
        Sprime = deux_opt(S, recuit=True)
    return Sprime


def temperature(t, fonction):
    """Applique la fonction temperature passée en argument à t

    Args:
        t (float):
        fonction (function): fonction de la température

    Returns:
        float: la temperature à l'instant t
    """
    return fonction(t)


def prob(dE: float, T: float):
    """Calcul

    Args:
        dE (float):différence d'energie calculée
        T (float): Température calculée

    Returns:
        la probabilité (float)
    """
    if dE < 0:  # si dE<0 alors distance_totale(Sprime)<distance_totale(S)
        # donc Sprime et plus interessant que S -> On le choisit avec une probas de 1
        return 1
    else:
        return np.exp(
            -dE / (T + 0.00001)
        )  # +0.00001 : pour eviter d'avoir une erreur si T=0


# Test avec differentes fonctions de températures (strictement positives et décroissantes)
A = 0.5
alpha = 0.99
fonction1 = lambda x: A * alpha**x
fonction2 = lambda x: 1.8 * (1 - x)
fonction1 = lambda x: 1.8 - 1.8 * np.cos()
fonction3 = lambda x: 1.8 / np.log(1 + x)


def recuit_simule(S0: np.array, kmax: int = 30000, fonction: callable = fonction2):
    """Fait le recuit_simule à partir d'une solution locale

    Args:
        S0 (np.array): Solution locale
        kmax (int, optional): Nombre de maximum d'itération Defaults to 30000.
        fonction (function, optional): la fonction qu'on va utiliser pour le calcul de température Defaults to fonction3.

    Returns:
        La nouvelle solution optimale ou non calculée par le recuit simule
    """
    S = S0
    for k in range(1, kmax):
        Sprime = voisin(S)
        # la condition d'acceptation du Sprime comme nouveau S depend de la proba et du hasard
        if prob(
            distance_totale(Sprime) - distance_totale(S),
            temperature(k / kmax, fonction),
        ) >= random.uniform(0, 1):
            S = Sprime
    return S

if __name__ == "__main__":
    coord = lire_fichier_coords("exemple2.txt")
    affiche_points(coord)
    tournee = recu
    affiche_tournee(tournee)
