import numpy as np
from common import lire_fichier


def reconstruire_texte(liste_mots: np.array, coupures: dict) -> tuple[str, int]:
    # Reconstruction du texte justifié
    lignes: list[str] = []
    fin = len(liste_mots)
    while fin > 0:
        debut = coupures.get(fin, 0)
        lignes.insert(0, " ".join(liste_mots[debut:fin]))
        fin = debut

    texte_justifie = "\n".join(lignes)
    return texte_justifie


def aux(
    longueurs_mots: np.array,
    memo: dict,
    coupures: dict,
    indice_mot_courant: int,
    largeur: int = 80,
) -> int:
    """
    Fonction auxiliaire pour calcul récursif avec memoïsation de la mise en forme justifiée.

    Args:
        longueurs_mots (np.array): longueurs de chaque mot du texte
        memo (dict): memoïsation des coûts déjà calculés
        coupures (dict): enregistrements des meilleures positions de coupure
        indice_mot_courant (int): nombre de mots considérés
        largeur (int): largeur maximale d'une ligne

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

    # Tester chaque position de début de ligne possible de manière décroissante
    for indice_debut in range(indice_mot_courant - 1, -1, -1):
        longueur_ligne = sum(longueurs_mots[indice_debut:indice_mot_courant]) + (
            indice_mot_courant - indice_debut - 1
        )

        # Comme on parcour de manière décroissante, des qu'on dépasse la largeur de la ligne, on est sur que les itérations suivantes seront non aussi supérieures à la largeur
        if longueur_ligne > largeur:
            break
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
    dp = [float("inf")] * (n + 1)
    coupures = {}
    dp[0] = 0

    # Pour chaque nouveau mot à insérer
    for i in range(1, n + 1):
        # On essaye d'insérer les mots d'avant sur la même ligne jusqu'à dépasser la largeur de la ligne
        for j in range(i - 1, -1, -1):
            longueur_ligne = sum(longueurs_mots[j:i]) + (i - j - 1)

            # Si on depasse la largeur de la ligne, alors pour les mots suivants aussi donc on break
            if longueur_ligne > largeur:
                break
            # On calcule le cout totale avec cette nouvelle solution potentielle, on utilise les couts des sous problèmes précédents
            cout = dp[j] + (largeur - longueur_ligne) ** 2

            # On garde le meilleur cout pour le `i`-eme mot
            if cout < dp[i]:
                dp[i] = cout
                coupures[i] = j
    cout_total = dp[-1]

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
