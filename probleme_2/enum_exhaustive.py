import common
import numpy as np
import copy

def somme_carre(ligne_actuel,taille_ligne):
    """Renvoie le calcul du nombre d'espace de fin de la ligne au carré

    Args:
        ligne_actuel (_type_): _description_
        taille_ligne (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (taille_ligne-sum(ligne_actuel))**2

def enum_exhaus(tableau,taille_ligne,ligne_actuel=[]):
    """Pas fonctionnel

    Args:
        tableau (_type_): _description_
        taille_ligne (_type_): _description_
        ligne_actuel (list, optional): _description_. Defaults to [].

    Returns:
        _type_: _description_
    """
    #cas de base
    if len(tableau)==0:
        return somme_carre(ligne_actuel,taille_ligne)
    #on fais le min entre retour ligne et rester sur la ligne, sauf qu'il est parfois impossible de faire l'un des deux 
    #si l'un des deux est impossible, sa valeur vaut inf et ducoup il ne dérange pas
    retour_ligne = float('inf')
    rester_sur_la_ligne = float('inf')
    #on passe à la ligne suivante
    if ligne_actuel!=[]:#seulement si la ligne n'est pas vide (évite le cas où on ajoute à l'infini des lignes vides)
        retour_ligne = somme_carre(ligne_actuel,taille_ligne)+enum_exhaus(tableau,taille_ligne)-1 #on fais donc le bilan de la ligne avec somme_carre
        #Notes : on ajoute pas de mots, juste on passe à la ligne
        #On soustrait 1 car le dernier mot de chaque ligne ne doit pas être suivi d'un espace (l'espace est placé par le cas ci-dessous)
    #on rajoute un mot sur la même ligne 
    if sum(ligne_actuel)+tableau[0]<=taille_ligne: #condition qui vérifie que le mot rentre sur la ligne
        rester_sur_la_ligne = 1+enum_exhaus(tableau[1:],taille_ligne,ligne_actuel+[tableau[0]])
        #on ajoute 1 car à la fin de chaque mot on met une espace
    return min(retour_ligne,rester_sur_la_ligne)

min_connu = float('inf')
meilleur_tableau = []

def enum_exhaus_mat(tableau,taille_ligne,ligne_actuel=[],matrice=[],somme_actu=0):
    #FONCTIONNE !!!!!
    #NOTES POUR MOI : ajouter le fait de compter les espaces entres les mots

    #cas de base
    if len(tableau)==0:
        #print(somme_actu)
        #print(matrice)
        global min_connu
        global meilleur_tableau
        somme_actu+=somme_carre(ligne_actuel,taille_ligne)
        matrice.append(ligne_actuel)
        if somme_actu<min_connu:
            min_connu=somme_actu
            meilleur_tableau=copy.deepcopy(matrice)
        matrice.pop()
        return 
    #reccurence
    #on passe à la ligne suivante
    if ligne_actuel!=[]:
        matrice.append(ligne_actuel)
        enum_exhaus_mat(tableau,taille_ligne,somme_actu=somme_actu+somme_carre(ligne_actuel,taille_ligne),matrice=matrice)
        matrice.pop()
    #on reste sur la même ligne si on peut 
    if sum(ligne_actuel)+tableau[0]<=taille_ligne:
        enum_exhaus_mat(tableau[1:],taille_ligne,ligne_actuel+[tableau[0]],somme_actu=somme_actu,matrice=matrice)
    #return min(retour_ligne,rester_sur_la_ligne)


fich = common.lire_fichier("recherche_complet.txt")[0]
print(fich[0])
fich = np.array([10,5,7,1,1])
#print(len(fich))
enum_exhaus_mat(fich,12)
print(meilleur_tableau)


fich = common.lire_fichier("recherche_complet.txt")[0]
print(fich[0])
fich = np.array([10,5,7,1,1])
print(enum_exhaus(fich,12))