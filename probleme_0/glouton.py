Hmin = 0
Hmax = int(10e9)


def optim_planning(demandes: list) -> list:
    """Algorithme glouton pour sélectionner un ensemble maximal de créneaux compatibles (sans chevauchement).
    On va insérer a chaque fois dans la liste_return la réservation avec la fin la plus tôt et ainsi de suite
    en vérifiant a chaque fois qu'il n'y a pas de chevauchement

    Args:
        demandes (list): liste de créneaux demandés

    Returns:
        list: la solution optimale au problème
    """

    assert type(demandes) == list, "verifie que demandes est bien une liste"

    if len(demandes) == 0:
        return []

    # Tri des demandes par heure de fin décroissante parce qu'on va prendre le dernier
    # élément de la liste a la place de la premiere car moins de complexité
    demande_trie = sorted(demandes, key=lambda x: x[1], reverse=True)

    liste_result = [demande_trie.pop()]

    for i in range(len(demande_trie)):
        # On récupère la prochaine plage qui finit le plus tot
        meilleur_plage = demande_trie.pop()
        debut_test, fin_test = (
            meilleur_plage  # On extrait le début et la fin du créneau à tester
        )

        # Verifie qu'elle est bien dans l'intervalle
        if debut_test < Hmin or fin_test > Hmax:
            return False
        # Si ce créneau commence après ou au moment où le dernier choisi se termine
        if liste_result[-1][1] <= debut_test:
            # Pas de chevauchement donc on peut l'ajouter à la liste return
            liste_result.append(meilleur_plage)

    return liste_result


exemple_demandes = ((2, 5), (7, 9), (3, 9), (2, 6), (4, 7))

demandes = [
    (1, 4),
    (3, 5),
    (0, 6),
    (5, 7),
    (3, 9),
    (5, 9),
    (6, 10),
    (8, 11),
    (8, 12),
    (2, 14),
    (12, 16),
    (1, 3),
    (0, 2),
    (6, 8),
    (5, 6),
    (3, 4),
    (9, 11),
    (11, 13),
    (13, 15),
    (14, 17),
]

# print(optim_planning(demandes))
