from enumeration import optim_planning as optim_planning_enum
from glouton import optim_planning as optim_planning_glouton
from generateurs import generateur_chevauchements_controle
import random

Hmin = 0
Hmax = int(10e9)

def testeur(reponse):
    # Trie les réservations par heure de début croissante
    reponse_triee = sorted(reponse, key=lambda x: x[0])
    i = 0
    N = len(reponse) - 1  # Dernier indice
    for k in reponse_triee:
        (debut, fin) = k  # On extrait le début et la fin de chaque réservation

        if i == 0:
            # Vérifie que le début de la première réservation est après Hmin
            if debut <= Hmin:
                return False
            fin_next = fin  # On garde en mémoire la fin actuelle pour comparaison suivante

        elif i == N:
            # Vérifie que la fin de la dernière réservation est avant Hmax
            if fin >= Hmax:
                return False

        else:
            # Vérifie qu'il n'y a pas de chevauchement entre les réservations
            if debut < fin_next:
                return False
            else:
                # Met à jour la fin actuelle pour la prochaine itération
                fin_next = fin
        i += 1

    # Si toutes les vérifications passent, la planification est valide
    return True


def generateur_base_de_donnees(Hmin,Hmax,nombre_de_reservations, nombre_de_planning):
    """
    Crée une liste de de forme [planning_1, planning_2 ...., planning_n] de taille nombre de planning
    chaque planning sera de la forme : planning = [reservation_1, reservation_2, ... reservation_n] de taille nombre_de_reservations
    les reservations seront générées aléatoire
    """
    donnees = [generateur_chevauchements_controle(nombre_de_reservations)for __ in range(nombre_de_planning)]
    return donnees

def comparateur(base_de_donnees):
    """
    Compare les deux fonctions d'optimisation : 
    - optim_planning_enum (version exhaustive)
    - optim_planning_glouton (version gloutonne)
    
    Pour chaque jeu de données de la base :
    - Vérifie la validité des résultats produits par les deux fonctions
    - Vérifie que les deux fonctions trouvent un résultat de même taille (nombre de réservations retenues)
    """
    for donnees in base_de_donnees:
        
        # Résultat considéré comme réelle avec l'exhaustivité
        reponse_vrai = optim_planning_enum(donnees)
        
        # Résultat a tester avec la methode glouton
        reponse_a_tester = optim_planning_glouton(donnees)
        
        # Vérifie la validité des réponses (pas de chevauchement, horaires valides)
        if testeur(reponse_vrai) == False:
            return False
        if testeur(reponse_a_tester) == False:
            return False

        # Vérifie que les deux méthodes retournent des résultats de même taille
        a = len(reponse_vrai) == len(reponse_a_tester)

        if not a:
            print(False)
            return False

    # Si toutes les vérifications passent
    print("Les deux fonctions sont valides et renvoient un résultat de même taille")
    return True


base_de_donnees = generateur_base_de_donnees(Hmin, Hmax, 5, 2)
#print(base_de_donnees)

comparateur(base_de_donnees)
