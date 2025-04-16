import random
import numpy as np

def generateur_donnee(n: int) -> np.array:
    """Génère des points entre -100 et 100

    Args:
        n (int): nombre de points

    Returns:
        list: liste de points à optimiser
    """
    return np.array([(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(n)])

