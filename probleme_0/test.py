from enumeration import optim_planning as optim_planning_enum
from glouton import optim_planning as optim_planning_glouton
import random

Hmin = 0
Hmax = int(10e9)


def comparateur(base_de_donnees):

    # print(len(base_de_donnees))

    for donnees in base_de_donnees:

        # print("Données", donnees)

        reponse_vrai = optim_planning_enum(donnees)
        reponse_a_tester = optim_planning_glouton(donnees)

        # print("Reponse_vrai",reponse_vrai)
        # print("Reponse a Tester",reponse_a_tester)
        a = len(reponse_vrai) == len(reponse_a_tester)

        # print(a)

        if not (a):
            print(False)
            return False

    print("les deux fonctions renvoient un")
    return True


base_de_donnees = generateur_base_de_donnees(Hmin, Hmax, 20, 200)
comparateur(base_de_donnees)
