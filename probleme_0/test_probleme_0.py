# %%
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import timeit

from glouton import optim_planning as optim_glouton, demandes
from enumeration import optim_planning as optim_enum, valide

def make_demandes(n):
    return demandes[:n]

# Liste des fonctions à comparer
fcts = [
    ("optim_glouton", lambda n: lambda: optim_glouton(make_demandes(n))),
    ("optim_enum",    lambda n: lambda: optim_enum(make_demandes(n)))
]

n_values = list(range(1, len(demandes) + 1))

plt.figure(figsize=(8, 6))

# Pour chaque fonction, on trace la courbe de complexité
for name, get_wrapper in fcts:
    times = []
    for n in n_values:
        t = timeit.timeit(get_wrapper(n), number=100)
        times.append(t)
    plt.plot(n_values, times, marker='o', label=name)

plt.xlabel("Taille de la liste de demandes")
plt.ylabel("Temps d'exécution (s)")
plt.title("Comparaison des complexités temporelles")
plt.legend()
plt.grid(True)
plt.show()
# %%
