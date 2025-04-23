import numpy as np
from common import lire_fichier


def aux(
    longueurs_mots: np.array,
    memo: dict,
    coupures: dict,
    indice_mot_courant: int,
    largeur: int = 80,
) -> int:
    """
    Fonction auxiliaire pour calcul récursif avec mémoïsation de la mise en forme justifiée.

    Args:
        longueurs_mots (np.array): longueurs de chaque mot du texte
        memo (dict): mémoïsation des coûts déjà calculés
        coupures (dict): enregistrements des meilleures positions de coupure
        indice_mot_courant (int): nombre de mots considérés (0..indice_mot_courant-1)
        largeur (int): largeur maximale d'une ligne (en caractères)

    Returns:
        int: coût minimal pour justifier les mots jusqu'à indice_mot_courant
    """
    # Cas de base
    if indice_mot_courant == 0:
        memo[0] = 0
        return 0

    # Renvoi si déjà calculé
    if indice_mot_courant in memo:
        return memo[indice_mot_courant]

    cout_minimal = float("inf")
    meilleure_coupure = 0

    # Tester chaque position de début de ligne possible
    for indice_debut in range(indice_mot_courant):
        longueur_ligne = sum(longueurs_mots[indice_debut:indice_mot_courant]) + (
            indice_mot_courant - indice_debut - 1
        )
        if longueur_ligne <= largeur:
            # coût induit par l'espace restant carré
            cout_espace = (largeur - longueur_ligne) ** 2
            cout_total = (
                aux(longueurs_mots, memo, coupures, indice_debut, largeur) + cout_espace
            )
            if cout_total < cout_minimal:
                cout_minimal = cout_total
                meilleure_coupure = indice_debut

    memo[indice_mot_courant] = cout_minimal
    coupures[indice_mot_courant] = meilleure_coupure
    return cout_minimal


def justifier(
    longueurs_mots: np.array, liste_mots: np.array, largeur: int = 80
) -> tuple[str, int]:
    """
    Justifie le texte fourni par liste_mots selon la largeur spécifiée.

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

    # Reconstruction du texte justifié
    lignes: list[str] = []
    fin = len(liste_mots)
    while fin > 0:
        debut = coupures.get(fin, 0)
        lignes.insert(0, " ".join(liste_mots[debut:fin]))
        fin = debut

    texte_justifie = "\n".join(lignes)
    return texte_justifie, cout_total


if __name__ == "__main__":
    longueurs_mots, liste_mots = lire_fichier("recherche_p1.txt")
    texte, cout = justifier(longueurs_mots, liste_mots, largeur=80)
    print(texte)
    print(f"\nCoût de justification : {cout}")
