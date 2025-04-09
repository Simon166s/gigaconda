import random


def generateur_non_chevauchant(n: int) -> list[tuple]:
    """Génère des intervalles chevauchant

    Args:
        n (int): nombre de créneaux

    Returns:
        list: tuple de créneaux dont on doit trouver la solution
    """
    return [(i, i + 1) for i in range(n)]


def generateur_chevauchements_controle(n: int) -> list[tuple]:
    """Génère des créneaux avec un chevauchement contrôlé (idéal pour tester les algos)

    Args:
        n (int): nombre de créneaux

    Returns:
        list[tuple]: liste de demandes de créneaux avec des chevauchements
    """
    donnees = []
    for _ in range(n):
        start = random.randint(0, 1000)
        duration = random.randint(1, 100)
        end = start + duration
        donnees.append((start, end))
    return sorted(donnees, key=lambda x: x[0])
