from common import *
import numpy as np
import copy


from common import *
import numpy as np
import copy


def somme_carre(longueur_ligne_courante: int, largeur_max: int, nb_espaces: int = 0):
    """Calcule le coût (carré de l'espace restant) d'une ligne en fonction de sa longueur

    Args:
        longueur_ligne_courante (int): somme des longueurs des mots présents sur la ligne
        largeur_max (int): largeur maximale autorisée pour une ligne
        nb_espaces (int, optional): nombre d'espaces entre les mots. Defaults to 0.

    Returns:
        int: coût associé à la ligne
    """
    return (largeur_max - longueur_ligne_courante - nb_espaces) ** 2


def enum_exhaus_memo(mots_restants: list, largeur_max: int, ligne_courante: list = []):
    """Effectue l'énumération exhaustive des possibilités avec mémoïsation

    Args:
        mots_restants (list): liste contenant les longueurs des mots restants à placer
        largeur_max (int): largeur maximale autorisée pour une ligne
        ligne_courante (list, optional): mots en cours d'écriture sur la ligne actuelle. Defaults to [].

    Returns:
        int: coût total minimal trouvé
    """
    global dictio_sous_opt

    # cas de base
    if len(mots_restants) == 0:
        return somme_carre(sum(ligne_courante), largeur_max, len(ligne_courante) - 1)

    # on fait le min entre retour à la ligne et rester sur la même ligne
    # (si l'une des deux options est impossible, elle vaut inf et n'influence pas le min)
    retour_ligne = float("inf")
    rester_sur_la_ligne = float("inf")

    # CAS 1 : on ajoute un mot sur la même ligne
    if sum(ligne_courante) + len(ligne_courante) - 1 + mots_restants[0] <= largeur_max:
        ligne_courante.append(mots_restants[0])
        rester_sur_la_ligne = enum_exhaus_memo(
            mots_restants[1:], largeur_max, ligne_courante
        )
        ligne_courante.pop()

    # CAS 2 : on change de ligne (uniquement si la ligne courante n’est pas vide)
    if ligne_courante != []:
        if len(mots_restants) in dictio_sous_opt:
            # on récupère le résultat mémoïsé
            retour_ligne = dictio_sous_opt[len(mots_restants)] + somme_carre(
                sum(ligne_courante), largeur_max, len(ligne_courante) - 1
            )
        else:
            # on calcule récursivement
            retour_ligne = enum_exhaus_memo(
                mots_restants, largeur_max, ligne_courante=[]
            )
            dictio_sous_opt[len(mots_restants)] = retour_ligne
            retour_ligne += somme_carre(
                sum(ligne_courante), largeur_max, len(ligne_courante) - 1
            )

    return min(retour_ligne, rester_sur_la_ligne)


def enum_exhaus_mat(
    mots_restants: list,
    largeur_max: int,
    ligne_courante: list = [],
    lignes_construites: list = [],
    cout_total_actuel: int = 0,
    longueur_ligne_courante: int = 0,
):
    """Effectue l'énumération exhaustive de toutes les mises en page possibles,
    en conservant la meilleure solution globale (stockée dans meilleur_tableau)

    Args:
        mots_restants (list): longueurs des mots restants à placer
        largeur_max (int): largeur maximale autorisée pour une ligne
        ligne_courante (list, optional): mots en cours d'écriture sur la ligne actuelle
        lignes_construites (list, optional): liste des lignes déjà validées
        cout_total_actuel (int, optional): coût cumulé jusqu'à maintenant
        longueur_ligne_courante (int, optional): somme des longueurs des mots sur la ligne actuelle

    Returns:
        None
    """
    # cas de base : plus de mots à traiter
    if len(mots_restants) == 0:
        global min_connu
        global meilleur_tableau
        # on ajoute le coût de la dernière ligne
        cout_total_actuel += somme_carre(
            longueur_ligne_courante, largeur_max, len(ligne_courante) - 1
        )
        lignes_construites.append(ligne_courante)
        # on conserve la solution si elle est meilleure
        if cout_total_actuel < min_connu:
            min_connu = cout_total_actuel
            meilleur_tableau = copy.deepcopy(lignes_construites)
        lignes_construites.pop()
        return

    # CAS 1 : on passe à la ligne suivante
    if ligne_courante != []:
        lignes_construites.append(ligne_courante)
        enum_exhaus_mat(
            mots_restants,
            largeur_max,
            ligne_courante=[],
            lignes_construites=lignes_construites,
            cout_total_actuel=cout_total_actuel
            + somme_carre(
                longueur_ligne_courante, largeur_max, len(ligne_courante) - 1
            ),
        )
        lignes_construites.pop()

    # CAS 2 : on reste sur la même ligne si c’est possible
    if (
        longueur_ligne_courante + mots_restants[0] + len(ligne_courante) - 1
        <= largeur_max
    ):
        mot = mots_restants[0]
        ligne_courante.append(mot)
        enum_exhaus_mat(
            mots_restants[1:],
            largeur_max,
            ligne_courante=ligne_courante,
            lignes_construites=lignes_construites,
            cout_total_actuel=cout_total_actuel,
            longueur_ligne_courante=longueur_ligne_courante + mot,
        )
        ligne_courante.pop()


def appel_enum_exhaus_mat(mots: list, largeur_max: int):
    """Initialise les variables globales et lance l'algorithme d'énumération exhaustive

    Args:
        mots (list): liste des longueurs des mots
        largeur_max (int): largeur maximale autorisée pour une ligne

    Returns:
        list: meilleure mise en page (liste de lignes)
    """
    global min_connu
    global meilleur_tableau
    min_connu = float("inf")
    meilleur_tableau = []
    enum_exhaus_mat(mots, largeur_max)
    return meilleur_tableau


# ======== TESTS ========
dictio_sous_opt = {}
test = np.array([10, 2, 2, 4, 6, 2, 5, 6])
print(enum_exhaus_memo(test, 20))  # Affiche la meilleure somme des carrés
print(appel_enum_exhaus_mat(test, 20))  # Affiche le meilleur tableau (mise en page)

dictio_sous_opt = {}
fich = lire_fichier("recherche_p1.txt")[0]
print(enum_exhaus_memo(fich, 80))  # Affiche la meilleure somme des carrés pour le fichier


