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

def comparateur(base_de_donnees):
    
    #print(len(base_de_donnees))
    
    for donnees in base_de_donnees:
        
        #print("Données", donnees)
        
        reponse_vrai = optim_planning_exh(donnees)
        reponse_a_tester = optim_planning(donnees)
        

        #print("Reponse_vrai",reponse_vrai)
        #print("Reponse a Tester",reponse_a_tester)
        a = len(reponse_vrai) == len(reponse_a_tester)
        
        #print(a)
        
        
        if not(a):
            print(False)
            return False
    
    print("les deux fonctions renvoient un")
    return True

base_de_donnees = generateur_base_de_donnees(Hmin,Hmax,20,200)
comparateur(base_de_donnees)