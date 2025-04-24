from common import *
import numpy as np
import copy

def somme_carre(longueur_ligne_actuel,taille_ligne,nb_espace=0):
    return (taille_ligne-longueur_ligne_actuel-nb_espace)**2

def enum_exhaus_memo(tableau,L,ligne_actuel=[]):
    global dictio_sous_opt
    """Effectue l'énumération exhaustive des possibilités avec mémoïsation

    Args:
        tableau (list): liste de liste contenant dans chaque sous-liste d'indice i la longueur des mots de la i-ème ligne
        taille_ligne (_type_): la taille d'une ligne (fixé)
        ligne_actuel (list, optional): Defaults to [].

    Returns:
        int: somme des carrés minimales
    """
    #cas de base
    if len(tableau)==0:
        return somme_carre(sum(ligne_actuel),L,len(ligne_actuel)-1)
    
    #on fais le min entre retour ligne et rester sur la ligne, sauf qu'il est parfois impossible de faire l'un des deux 
    #si l'un des deux est impossible, sa valeur vaut inf et ducoup il ne dérange pas
    retour_ligne = float('inf')
    rester_sur_la_ligne = float('inf')
    #CAS 1 : on ajoute un mot sur la même ligne
    if sum(ligne_actuel)+len(ligne_actuel)-1+tableau[0]<=L: #condition qui vérifie que le mot rentre sur la ligne
        ligne_actuel.append(tableau[0])
        rester_sur_la_ligne = enum_exhaus_memo(tableau[1:],L,ligne_actuel)
        ligne_actuel.pop()
    #CAS 2 : on change de ligne (sans ajouter de mot)
    if ligne_actuel!=[]:#seulement si la ligne n'est pas vide (évite le cas où on ajoute à l'infini des lignes vides)
        if len(tableau) in dictio_sous_opt.keys(): #si le sous-problème a déjà été traité
            retour_ligne = dictio_sous_opt[len(tableau)]+somme_carre(sum(ligne_actuel),L,len(ligne_actuel)-1)
        else: #sinon 
            retour_ligne = enum_exhaus_memo(tableau,L,ligne_actuel=[])
            dictio_sous_opt[len(tableau)]=retour_ligne #on met à jour le dictionnaire
            retour_ligne+=somme_carre(sum(ligne_actuel),L,len(ligne_actuel)-1)#on fais donc le bilan de la ligne avec somme_carre
    return min(retour_ligne,rester_sur_la_ligne)

dictio_sous_opt = {}
test = np.array([10,2,2,4,6,2,5,6])
print(enum_exhaus_memo(test,20))

dictio_sous_opt = {}
fich = common.lire_fichier("recherche_p1.txt")[0]
print(enum_exhaus_memo(fich,80))



def enum_exhaus_mat(
    tableau, taille_ligne, ligne_actuel=[], matrice=[], somme_actu=0, l_ligne_actu=0
):
    """Effectue l'énumération exhaustive des possibilités pour trouver la solution optimale
    La solution optimale est stockée dans la variable global meilleur_tableau

    Args:
        tableau (list): liste de liste contenant dans chaque sous-liste d'indice i la longueur des mots de la i-ème ligne
        taille_ligne (_type_): la taille d'une ligne (fixé)

    Returns:
        None
    """
    #cas de base
    if len(tableau)==0:

        global min_connu
        global meilleur_tableau
        # Ne conserve la matrice que si elle est meilleure que la meilleure matrice trouvée jusqu'à présent
        somme_actu += somme_carre(l_ligne_actu, taille_ligne, len(ligne_actuel) - 1)
        matrice.append(ligne_actuel)
        if somme_actu<min_connu:
            min_connu=somme_actu
            meilleur_tableau=copy.deepcopy(matrice)
        matrice.pop()
        return

    # On passe à la ligne suivante
    if ligne_actuel != []:
        matrice.append(ligne_actuel)
        enum_exhaus_mat(
            tableau,
            taille_ligne,
            somme_actu=somme_actu
            + somme_carre(l_ligne_actu, taille_ligne, len(ligne_actuel) - 1),
            matrice=matrice,
            ligne_actuel=[],
        )
        matrice.pop()
    # On reste sur la même ligne si on peut
    if (
        l_ligne_actu + tableau[0] + len(ligne_actuel) - 1 <= taille_ligne
    ):  # Condition qui vérifie que le mot rentre sur la ligne
        t_0 = tableau[0]
        ligne_actuel.append(t_0)
        enum_exhaus_mat(
            tableau[1:],
            taille_ligne,
            ligne_actuel,
            somme_actu=somme_actu,
            matrice=matrice,
            l_ligne_actu=l_ligne_actu + t_0,
        )
        ligne_actuel.pop()
    return


def appel_enum_exhaus_mat(tableau, taille_ligne):
    global min_connu
    global meilleur_tableau
    min_connu = float("inf")
    meilleur_tableau = []
    enum_exhaus_mat(tableau, taille_ligne)
    return meilleur_tableau

fich = np.array([10,2,2,4,6,2,5,6])
print(appel_enum_exhaus_mat(fich,20))