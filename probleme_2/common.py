import numpy as np


def lire_fichier(nom_fichier: str) -> tuple[np.array]:
    """Lit le fichier de texte et renvoie la liste des longueurs de chaque mots associée

    Args:
        nom_fichier (str): le nom du fichier dont on veut extraire le texte

    Raises:
        ValueError: levée d'erreur si l'extraction n'est pas possible car cela veut dire que le fichier est mal formé

    Returns:
        tuple[np.array]: tuple contenant:
            -la matrice ligne des longueurs de chaque mot du texte
            -la matrice ligne des mot du texte
    """
    mots = []
    longueurs_mots = []
    with open(nom_fichier) as f:
        try:
            for ligne in f:
                if not ligne.isspace():
                    for mot in ligne.split(" "):
                        longueurs_mots.append(len(mot))
                        mots.append(mot)
        except:
            raise ValueError("Fichier de coordonnées mal formé")
    return np.array(longueurs_mots), np.array(mots)


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
