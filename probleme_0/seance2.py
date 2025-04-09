import numpy as np
def valide(creneau_test, curr):
    
    debut_test, fin_test = creneau_test
    if creneau_test in curr :
        return False
    for creneau in curr:
        debut, fin = creneau
        if not (fin_test <= debut or debut_test >= fin):
            return False
        
    return True

class valideur:
    def __init__(self,creneau_min,creneau_max):
        #print(creneau_max)
        self.agenda = np.array([0 for a in range(0,creneau_max)])
    def get_maj_possible(self,creneau):
        hd,hf=creneau
        if 1 not in self.agenda[hd:hf]:
            return True

    def maj(self,creneau):
        hd,hf=creneau
        #print(hd,hf)
        self.agenda[hd:hf]=1
        

def optim_planning(demandes):
    demande_trie = sorted(demandes,key=lambda x:x[1],reverse=True)
    #print(demande_trie)
    liste_result = []    
    V = valideur(min(demandes,key= lambda x:x[0])[0],max(demandes,key= lambda x:x[1])[1])
    for i in range(len(demande_trie)):
        meilleur_plage = demande_trie.pop()
        if V.get_maj_possible(meilleur_plage):
            liste_result.append(meilleur_plage)
            V.maj(meilleur_plage)
    print(V.agenda)
    return sorted(liste_result,key=lambda x:x[0])

exemple_demandes = ((2,5),(7,9),(3,9),(2,6),(4,7))

demandes = [
    (1, 4), (3, 5), (0, 6), (5, 7), (3, 9),
    (5, 9), (6, 10), (8, 11), (8, 12), (2, 14),
    (12, 16), (1, 3), (0, 2), (6, 8), (5, 6),
    (3, 4), (9, 11), (11, 13), (13, 15), (14, 17)
]

print(optim_planning(demandes))

    