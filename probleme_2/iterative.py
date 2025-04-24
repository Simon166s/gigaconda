import numpy as np
from common import lire_fichier, reconstruire_texte

# ---------------------------
# Implémentation itérative via la programmation dynamique
# ---------------------------


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


# A l'éxécution
if __name__ == "__main__":
    longueurs_mots, liste_mots = lire_fichier("recherche_p1.txt")
    print("=" * 30 + " VERSION ITERATIVE " + "=" * 30 + "\n")
    texte_iter, cout_iter = justifier_iteratif(longueurs_mots, liste_mots, largeur=80)
    print(texte_iter)
    print(f"\nCoût de justification : {cout_iter}")
