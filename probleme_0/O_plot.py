# %%
import perfplot
from enumeration import optim_planning as optim_enum
from glouton import optim_planning as optim_glouton
from generateurs import generateur_chevauchements_controle
import numpy as np

# Générateur de données adapté à la taille n
def generate_input(n):
    # Assure-toi que generateur_chevauchements_controle(n) renvoie un objet pour lequel len() fonctionne
    data = generateur_chevauchements_controle(n)
    return list(data)  # si besoin de forcer une liste

# Kernel de référence qui calcule n*2**n à partir des données.
def reference_kernel(data):
    n = len(data)
    return n * 2**n

perfplot.show(
    setup=generate_input,
    kernels=[optim_glouton],
    labels=["optim_glouton"],
    n_range= [10**k for k in range(1,8)],  # Plage de tailles d'entrée
    xlabel="Taille de l'entrée (n)",
    logx=True,           # Pour une meilleure visualisation en échelle logarithmique
    logy=True,
)

# %%
