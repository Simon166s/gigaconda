import numpy as np
from common import *


words_length = lire_fichier("recherche_p1.txt")

def aux(words_length: np.array, d: dict, current_word: int, L: int = 80) -> int:
    if current_word is None:
        current_word = len(words_length)

    if current_word in d:
        return d[current_word]
    # Cas de base 
    if current_word == 0:
        d[0] = 0
        return d[0]
    min_error = float("inf")
    # On teste toutes les façons de faire une ligne se terminant à current_word
    for i in range(current_word):
        line_length = sum(words_length[i:current_word]) + (current_word - i - 1)
        if line_length <= L:
            left_space_error = (L - line_length) ** 2
            total_error = aux(words_length, d, i, L) + left_space_error
            min_error = min(min_error, total_error)


    d[current_word] = min_error
    return min_error

def indent_recu(words_length: np.array, L: int = 80):
    d = {}
    aux(words_length, d, len(words_length))
    
print(aux(words_length))
print(reconstruire_texte())
