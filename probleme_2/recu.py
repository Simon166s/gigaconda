import numpy as np
from common import lire_fichier, reconstruire_texte

# ---------------------------
# Implémentation Récursive mémoisée
# ---------------------------


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
        longueur_ligne = sum(longueurs_mots[j:i]) + (i - j - 1)

        # Comme on parcours de manière décroissante, des qu'on dépasse la largeur de la ligne, on est sur que les itérations suivantes seront non aussi supérieures à la largeur
        if longueur_ligne > largeur:
            break
        # coût induit par l'espace restant carré
        cout_espace = (largeur - longueur_ligne) ** 2
        cout_total = aux(longueurs_mots, memo, coupures, j, largeur) + cout_espace
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


# A l'éxécution:
if __name__ == "__main__":
    longueurs_mots, liste_mots = lire_fichier("recherche_p1.txt")
    print("=" * 31 + " VERSION RECURSIVE" + "=" * 31 + "\n")
    texte_recu, cout_recu = justifier_recu(longueurs_mots, liste_mots, largeur=80)
    print(texte_recu)
    print(f"\nCoût de justification : {cout_recu}")
