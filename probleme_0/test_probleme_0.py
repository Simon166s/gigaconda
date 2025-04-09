import timeit
import matplotlib.pyplot as pl
import numpy as np
from random import *


########################################################################################################
# Comparaison des complexités
########################################################################################################
pl.subplot(2,1,2)
taille = 50
# Différentes tailles pour tracé de courbes
n = range(taille//40, taille, taille//40)

# liste des fonctions à comparer
liste_fct = [] 

for fct in liste_fct:
    print(fct.__name__)
    d = []
    Y = []
    for i in n:
        d.append( timeit.timeit("fct()", globals=globals(), number=100))
    Y.append(np.array(d))

    p, = pl.plot(n, Y[0], label = fct.__name__)
    pl.fill_between(n, Y[1], Y[2], color = pl.getp(p, 'color'), alpha=0.5)

pl.legend(loc=2)
pl.xlabel('taille')
pl.ylabel('durée [s]')
pl.show()