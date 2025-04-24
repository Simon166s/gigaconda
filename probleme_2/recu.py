import numpy as np
from common import lire_fichier


def reconstruire_texte(liste_mots: np.ndarray, coupures: dict[int, int]) -> str:
    """
    Reconstruit le texte justifié à partir de la liste de mots et des positions de coupure.

    Args:
        liste_mots (np.ndarray):
            Tableau contenant les mots du texte d'origine
        coupures (dict[int, int]):
            Dictionnaire qui associe chaque index de fin de ligne (exclu)
            à l'index de début de cette même ligne.

    Returns:
        str:
            Le texte justifié sous forme d'une chaîne de caractères, avec
            chaque ligne séparée par un saut de ligne.
    """
    lignes: list[str] = []
    fin = len(liste_mots)
    # Traiter tous les mots 
    while fin > 0:
        # On récupère où commence la dernière ligne
        debut = coupures.get(fin, 0)
        # On assemble la ligne à partir de debut jusqu'à fin (exclu)
        lignes.insert(0, " ".join(liste_mots[debut:fin]))
        # On recule la borne supérieure pour traiter la ligne précédente
        fin = debut

    # On joint toutes les lignes par un retour à la ligne
    texte_justifie = "\n".join(lignes)
    return texte_justifie


def aux(
    longueurs_mots: np.array,
    memo: dict,
    coupures: dict,
    i: int,
    largeur: int = 80,
) -> int:
    """
    Fonction auxiliaire pour calcul récursif avec memoïsation de la mise en forme justifiée.

    Args:
        longueurs_mots (np.array): longueurs de chaque mot du texte
        memo (dict): memoïsation des coûts déjà calculés
        coupures (dict): enregistrements des meilleures positions de coupure
        i (int): nombre de mots considérés
        largeur (int): largeur maximale d'une ligne

    Returns:
        int: coût minimal pour justifier les mots jusqu'au `i`-ème mot
    """
    # Cas de base
    if i == 0:
        memo[0] = 0
        return 0

    # Renvoi si déjà calculé
    if i in memo:
        return memo[i]

    cout_minimal = float("inf")
    meilleure_coupure = 0

    # Tester chaque position de début de ligne possible de manière décroissante
    for j in range(i - 1, -1, -1):
        longueur_ligne = sum(longueurs_mots[j:i]) + (
            i - j - 1
        )

        # Comme on parcours de manière décroissante, des qu'on dépasse la largeur de la ligne, on est sur que les itérations suivantes seront non aussi supérieures à la largeur
        if longueur_ligne > largeur:
            break
        # coût induit par l'espace restant carré
        cout_espace = (largeur - longueur_ligne) ** 2
        cout_total = (
            aux(longueurs_mots, memo, coupures, j, largeur) + cout_espace
        )
        if cout_total < cout_minimal:
            cout_minimal = cout_total
            meilleure_coupure = j

    memo[i] = cout_minimal
    coupures[i] = meilleure_coupure
    return cout_minimal


def justifier_recu(
    longueurs_mots: np.array, liste_mots: np.array, largeur: int = 80
) -> tuple[str, int]:
    """
    Justifie le texte fourni par liste_mots selon la largeur spécifiée
    de manière récursive avec la fonction `aux`

    Args:
        longueurs_mots (np.array): longueurs de chaque mot
        liste_mots (np.array): mots du texte
        largeur (int): largeur maximale d'une ligne

    Returns:
        tuple[str, int]:
            - texte justifié (chaîne avec retours à la ligne)
            - coût total de justification
    """
    memo = {}
    coupures = {}

    # Calcul du coût minimal et remplissage de coupures
    cout_total = aux(longueurs_mots, memo, coupures, len(longueurs_mots), largeur)
    texte_justifie = reconstruire_texte(liste_mots, coupures)
    return texte_justifie, cout_total


def justifier_iteratif(
    longueurs_mots: np.array, liste_mots: np.array, largeur: int = 80
) -> tuple[str, int]:
    """Justifie le texte fourni par `liste_mots` selon la largeur spécifiée de manière
    itérative en utilisant la programmatino dynamique

    Args:
        longueurs_mots (np.array): longueurs de chaque mot
        liste_mots (np.array): mots du texte
        largeur (int): largeur maximale d'une ligne

    Returns:
        tuple[str, int]:
            - texte justifié (chaîne avec retours à la ligne)
            - coût total de justification
    """

    n = len(longueurs_mots)
    liste_des_couts = [float("inf")] * (n + 1)
    coupures = {}
    liste_des_couts[0] = 0

    # Pour chaque nouveau mot à insérer
    for i in range(1, n + 1):
        # On essaye d'insérer les mots d'avant sur la même ligne jusqu'à dépasser la largeur de la ligne
        for j in range(i - 1, -1, -1):
            longueur_ligne = sum(longueurs_mots[j:i]) + (i - j - 1)

            # Si on depasse la largeur de la ligne, alors pour les mots suivants aussi donc on break
            if longueur_ligne > largeur:
                break
            # On calcule le cout totale avec cette nouvelle solution potentielle, on utilise les couts des sous problèmes précédents
            cout = liste_des_couts[j] + (largeur - longueur_ligne) ** 2

            # On garde le meilleur cout pour le `i`-eme mot
            if cout < liste_des_couts[i]:
                liste_des_couts[i] = cout
                coupures[i] = j
    cout_total = liste_des_couts[-1]

    # Reconstruit le texte à partir du dictionnaire des coupures
    texte_justifie = reconstruire_texte(liste_mots, coupures)
    return texte_justifie, cout_total


if __name__ == "__main__":
    longueurs_mots, liste_mots = lire_fichier("recherche_p1.txt")
    print("=" * 10 + "VERSION RECU" + "=" * 10)
    texte_recu, cout_recu = justifier_recu(longueurs_mots, liste_mots, largeur=80)
    print(texte_recu)
    print(f"\nCoût de justification : {cout_recu}")
    print("=" * 10 + "VERSION ITER" + "=" * 10)
    texte_iter, cout_iter = justifier_iteratif(longueurs_mots, liste_mots, largeur=80)
    print(texte_iter)
    print(f"\nCoût de justification : {cout_iter}")
