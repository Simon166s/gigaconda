from probleme_0 import optim_planning_exh
from seance2 import optim_planning
import random

Hmin =0
Hmax = int(10E9)

def generateur_base_de_donnees(Hmin,Hmax,nombre_de_donnees, nombre_de_resultats):
    donnees = [
    [
        sorted([random.randint(Hmin, Hmax), random.randint(Hmin, Hmax)])
        for _ in range(nombre_de_donnees)
    ]
    for __ in range(nombre_de_resultats)
]
    return donnees

def testeur(reponse):
    reponse_triee = sorted(reponse,key=lambda x:x[0])
    i = 0
    N = len(reponse)-1
    for k in reponse_triee:
        (debut,fin) = k
        if i == 0 :
            if debut < Hmin :
                return False
            fin_next = fin
        elif i == N:
            if fin > Hmax :
                return False
        
        else : 
            if debut < fin_next :
                return False
            else :
                fin_next = fin
        i+=1
    
    return True
        
    
    
def comparateur(base_de_donnees):
    
    #print(len(base_de_donnees))
    
    for donnees in base_de_donnees:
        
        #print("Données", donnees)
        
        reponse_vrai = optim_planning_exh(donnees)
        reponse_a_tester = optim_planning(donnees)
        
        if testeur(reponse_vrai) == False :
            return False
        if testeur(reponse_a_tester) == False :
            return False
            
        #print("Reponse_vrai",reponse_vrai)
        #print("Reponse a Tester",reponse_a_tester)
        
        a = len(reponse_vrai) == len(reponse_a_tester)
        
        #print(a)
        
        
        if not(a):
            print(False)
            return False
    
    print("les deux fonctions renvoient un resultat de meme longueur et valide")
    return True

base_de_donnees = generateur_base_de_donnees(Hmin,Hmax,10,200)
comparateur(base_de_donnees)