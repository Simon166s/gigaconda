Hmin = 0
Hmax = 10E9

# ? est ce qu ón doit faire ca 
# ! Attention
# TODO change implementation 

def duree_planning(planning):
    if not(planning):
        return float("-inf")
    total = 0
    for k in planning :
        (debut,fin) = k
        total += fin-debut
 
    return total
        
def valide(creneau_test, curr):
    
    debut_test, fin_test = creneau_test
    if creneau_test in curr :
        return False
    for creneau in curr:
        debut, fin = creneau
        if not (fin_test <= debut or debut_test >= fin):
            return False
        
    return True
        
def optim_planning(demandes, curr = []):
    
    demandes = list(demandes)
    
    plannings=[]
    
    for creneau in demandes :
        if valide(creneau,curr)  :
            curr.append(creneau)
            plannings.append(optim_planning(demandes,curr))
            curr.pop()
    
    print(plannings)
    print(curr)
    if plannings :
        
        return max(plannings, key=duree_planning)
    else :
        return None

exemple_demandes = ((2,5),(7,9),(3,9),(2,6),(4,7))

print(optim_planning(exemple_demandes))