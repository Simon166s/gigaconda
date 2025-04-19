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
    return np.array(longueurs_mots), np.array(mot)


def remplir_matrice_depuis_longueurs(mots: np.array, matrice_longueurs: np.array) -> np.array:
    """Reconstitue la matrice de mots à partir de la matrice de tailles
    et de la liste ordonnée des mots.

    Args:
        mots (np.array): la matrice ligne des mots du texte
        matrice_longueurs (np.array): la matrice des longueurs que l'on a optimisée

    Returns:
        np.array: la matrice contenant les mots arrangés à partir de la matrice des longueurs
    """    
    l, L = matrice_longueurs.shape
    matrice_mots = np.full((l, L), "", dtype=object)

    index_mot = 0
    l, L = matrice_longueurs.shape
    matrice_mots = np.empty((l, L), dtype=object)
    index_mot = 0
    for i in range(l):
        for j in range(L):
            if matrice_longueurs[i, j] > 0:
                matrice_mots[i, j] = mots[index_mot]
                index_mot += 1
            else:
                matrice_mots[i, j] = ""
    return matrice_mots

mots = ["a,", "bb", "cc"]
matrice_longueur = np.array([[2, 0],[2, 2]])
matrice_de_mot = remplir_matrice_depuis_longueurs(mots, matrice_longueur)
print(matrice_de_mot)

def reconstruire_texte(matrice: np.array) -> str:
    """Reconstruir un texte à partir d'une matrice de mots

    Args:
        matrice (np.array): _description_

    Returns:
        str: _description_
    """    
    lignes = []
    for ligne in matrice:
        mots_valides = [mot for mot in ligne if mot]
        lignes.append(" ".join(mots_valides))
    return "\n".join(lignes)

print(reconstruire_texte(matrice_de_mot))


