Hmin = 0
Hmax = 10e9


def valide(creneau_test, curr):
    """
    Vérifie si une reservation peut être ajouté à une liste de reservations existante
    sans qu'il y ait de chevauchement.
    """

    debut_test, fin_test = (
        creneau_test  # On extrait le début et la fin du créneau à tester
    )

    if debut_test < Hmin or fin_test > Hmax:
        return False

    # Si le créneau est déjà présent dans la liste actuelle, on le refuse
    if creneau_test in curr:
        return False

    # On vérifie les conflits avec tous les créneaux déjà choisis
    for creneau in curr:
        debut, fin = creneau

        # Test de non-chevauchement :
        # Si fin_test <= debut est FALSE ou Si debut_test >= fin est FALSE
        # Alors, il y a chevauchement et on retourne False
        if not (fin_test <= debut or debut_test >= fin):
            return False

    # Si aucun conflit n’a été trouvé c'est validé
    return True


def optim_planning(demandes: list, curr: list = []) -> tuple:
    """
    Fonction récursive d'optimisation complète (énumération exhaustive).
    qui va renvoyer la plus grande liste possible de créneaux non chevauchants
    """

    plannings = []  # Stocke toutes les combinaisons valides explorées
    a = 0  # Compteur de branches valides explorées

    for creneau in demandes:

        # Vérifie si ce créneau peut être ajouté à la liste actuelle
        if valide(creneau, curr):
            a += 1
            curr.append(creneau)  # Ajoute le créneau à la solution actuelle
            # Appelle récursivement la fonction pour poursuivre l'exploration
            plannings.append(optim_planning(demandes, curr))
            curr.pop()  # Backtracking

    # Si aucun créneau ne peut être ajouté (fin de branche), retourne une copie de la solution actuelle
    if a == 0:
        return curr.copy()

    # Retourne la solution avec le plus grand nombre de créneaux
    return max(plannings, key=len)


exemple_demandes = [(2, 5), (7, 9), (3, 9), (2, 6), (4, 7)]
# print(optim_planning(exemple_demandes))
