import common
import numpy as np
import copy

def somme_carre(longueur_ligne_actuel,taille_ligne,nb_espace=0):
    """Renvoie le calcul du nombre d'espace de fin de la ligne au carré

    Args:
        ligne_actuel (_type_): _description_
        taille_ligne (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (taille_ligne-longueur_ligne_actuel-nb_espace)**2

def enum_exhaus(tableau,L,ligne_actuel=[],t_taille_ligne=[]):
    global dictio_sous_opt
    """Pas fonctionnel

    Args:
        tableau (_type_): _description_
        taille_ligne (_type_): _description_
        ligne_actuel (list, optional): _description_. Defaults to [].

    Returns:
        _type_: _description_
    """
    print(ligne_actuel)
    #cas de base
    if len(tableau)==0:
        return somme_carre(sum(ligne_actuel),L,len(ligne_actuel)-1)
    if len(tableau) in dictio_sous_opt.keys():
        return dictio_sous_opt[len(tableau)]
    
    #on fais le min entre retour ligne et rester sur la ligne, sauf qu'il est parfois impossible de faire l'un des deux 
    #si l'un des deux est impossible, sa valeur vaut inf et ducoup il ne dérange pas
    retour_ligne = float('inf')
    rester_sur_la_ligne = float('inf')
    #print(t_taille_ligne)
    #print(tableau)
    #on passe à la ligne suivante

    if sum(ligne_actuel)+len(ligne_actuel)-1+tableau[0]<=L: #condition qui vérifie que le mot rentre sur la ligne
        ligne_actuel.append(tableau[0])
        rester_sur_la_ligne = enum_exhaus(tableau[1:],L,ligne_actuel,t_taille_ligne)
        ligne_actuel.pop()
        #on ajoute 1 car à la fin de chaque mot on met une espace
    if ligne_actuel!=[]:#seulement si la ligne n'est pas vide (évite le cas où on ajoute à l'infini des lignes vides)
        t_taille_ligne.append(sum(ligne_actuel))
        retour_ligne = somme_carre(sum(ligne_actuel),L,len(ligne_actuel)-1)+enum_exhaus(tableau,L,ligne_actuel=[],t_taille_ligne=t_taille_ligne) #on fais donc le bilan de la ligne avec somme_carre
        t_taille_ligne.pop()
        #Notes : on ajoute pas de mots, juste on passe à la ligne
        #On soustrait 1 car le dernier mot de chaque ligne ne doit pas être suivi d'un espace (l'espace est placé par le cas ci-dessous)
    #on rajoute un mot sur la même ligne 
    min_actu = min(retour_ligne,rester_sur_la_ligne)
    #dictio_sous_opt[len(tableau)]=min_actu
    #print(t_taille_ligne)
    #print(min_actu)
    return min_actu


#test = np.array([10,2,2,4,6,2,5,6])
#print(enum_exhaus(test,20))


mimimum = float('inf')
tableau_r = []

dictio_sous_opt = {}
def enum_exhaus_memo(tableau,L,ligne_actuel=[],t_taille_ligne=[]):
    global dictio_sous_opt
    """Pas fonctionnel

    Args:
        tableau (_type_): _description_
        taille_ligne (_type_): _description_
        ligne_actuel (list, optional): _description_. Defaults to [].

    Returns:
        _type_: _description_
    """
    print(ligne_actuel)
    #cas de base
    if len(tableau)==0:
        return somme_carre(sum(ligne_actuel),L,len(ligne_actuel)-1)
    
    #on fais le min entre retour ligne et rester sur la ligne, sauf qu'il est parfois impossible de faire l'un des deux 
    #si l'un des deux est impossible, sa valeur vaut inf et ducoup il ne dérange pas
    retour_ligne = float('inf')
    rester_sur_la_ligne = float('inf')
    #print(t_taille_ligne)
    #print(tableau)
    #on passe à la ligne suivante

    if sum(ligne_actuel)+len(ligne_actuel)-1+tableau[0]<=L: #condition qui vérifie que le mot rentre sur la ligne
        ligne_actuel.append(tableau[0])
        rester_sur_la_ligne = enum_exhaus_memo(tableau[1:],L,ligne_actuel,t_taille_ligne)
        ligne_actuel.pop()
        #on ajoute 1 car à la fin de chaque mot on met une espace
    if ligne_actuel!=[]:#seulement si la ligne n'est pas vide (évite le cas où on ajoute à l'infini des lignes vides)
        if len(tableau) in dictio_sous_opt.keys():
            retour_ligne = dictio_sous_opt[len(tableau)]+somme_carre(sum(ligne_actuel),L,len(ligne_actuel)-1)
        else: 
            #t_taille_ligne.append(sum(ligne_actuel))
            retour_ligne = enum_exhaus_memo(tableau,L,ligne_actuel=[],t_taille_ligne=t_taille_ligne) #on fais donc le bilan de la ligne avec somme_carre
            #if retour_ligne<rester_sur_la_ligne:
            dictio_sous_opt[len(tableau)]=retour_ligne
            retour_ligne+=somme_carre(sum(ligne_actuel),L,len(ligne_actuel)-1)
            #t_taille_ligne.pop()
        #Notes : on ajoute pas de mots, juste on passe à la ligne
        #On soustrait 1 car le dernier mot de chaque ligne ne doit pas être suivi d'un espace (l'espace est placé par le cas ci-dessous)
    #on rajoute un mot sur la même ligne 
    min_actu = min(retour_ligne,rester_sur_la_ligne)
    #print(t_taille_ligne)
    #print(min_actu)
    return min_actu

test = np.array([10,2,2,4,6,2,5,6])
print(enum_exhaus_memo(test,20))
print(dictio_sous_opt)
print(tableau_r)


min_connu = float('inf')
meilleur_tableau = []

def enum_exhaus_mat(tableau,taille_ligne,ligne_actuel=[],matrice=[],somme_actu=0,l_ligne_actu=0):
    #FONCTIONNE !!!!!
    #NOTES POUR MOI : ajouter le fait de compter les espaces entres les mots

    #cas de base
    if len(tableau)==0:
        print(somme_actu)
        #print(matrice)
        global min_connu
        global meilleur_tableau
        somme_actu+=somme_carre(l_ligne_actu,taille_ligne,len(ligne_actuel)-1)
        matrice.append(ligne_actuel)
        if somme_actu<min_connu:
            print("pass")
            min_connu=somme_actu
            meilleur_tableau=copy.deepcopy(matrice)
        matrice.pop()
        return 
    #reccurence
    #on passe à la ligne suivante
    #print(tableau)
    if ligne_actuel!=[]:
        matrice.append(ligne_actuel)
        enum_exhaus_mat(tableau,taille_ligne,somme_actu=somme_actu+somme_carre(l_ligne_actu,taille_ligne,len(ligne_actuel)-1),matrice=matrice,ligne_actuel=[])
        matrice.pop()
    #on reste sur la même ligne si on peut 
    if l_ligne_actu+tableau[0]+len(ligne_actuel)-1<=taille_ligne:
        t_0 = tableau[0]
        ligne_actuel.append(t_0)
        enum_exhaus_mat(tableau[1:],taille_ligne,ligne_actuel,somme_actu=somme_actu,matrice=matrice,l_ligne_actu=l_ligne_actu+t_0)
        ligne_actuel.pop()
        #return min(retour_ligne,rester_sur_la_ligne)
    return 


# #fich = common.lire_fichier("recherche_p1.txt")[0]
# #print(fich)
fich = np.array([10,2,2,4,6,2,5,6])
# #print(len(fich))
enum_exhaus_mat(fich,20)
print(meilleur_tableau)
print(min_connu)


"""fich = common.lire_fichier("recherche_complet.txt")[0]
print(fich[0])
fich = np.array([10,5,7,1,1])
print(enum_exhaus(fich,12))"""