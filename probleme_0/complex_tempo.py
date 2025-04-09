import matplotlib.pyplot as plt
import timeit
import numpy as np

from glouton import optim_planning as optim_glouton
from enumeration import optim_planning as optim_enum, valide
from generateurs import generateur_non_chevauchant, generateur_chevauchements_controle


class ComplexiteTempo:
    def __init__(
        self,
        functions_dict: dict = None,
        generateur=generateur_non_chevauchant,
    ):
        """
        Initialise l'objet avec le nombre maximum de demandes à tester et la liste des fonctions à évaluer.

        :param nbr_of_demand: Nombre maximum de demandes (taille maximale pour les tests)
        :param functions_dict: Dictionnaire avec pour clé le nom de la fonction et pour valeur la fonction elle-même.
                               Par défaut, on compare 'optim_glouton' et 'optim_enum'.
        """
        self.generateur = generateur
        # Si aucun dictionnaire de fonctions n'est fourni, utiliser les fonctions par défaut
        if functions_dict is None:
            self.functions_dict = {
                "Optimisation Glouton": optim_glouton,
                "Optimisation par énumération exhaustive": optim_enum,
            }
        else:
            self.functions_dict = functions_dict

    def wrapper(self, func, n):
        """
        Génère une fonction sans argument qui exécute `func` sur un jeu de données
        généré par generateur_base_de_donnees pour une taille donnée `n`.
        """
        data = self.generateur(n)
        return lambda: func(data)

    def benchmark_function(self, func, n_values, number=100):
        """
        Mesure le temps d'exécution de la fonction `func` pour une liste de tailles `n_values`.
        Chaque test est répété `number` fois pour obtenir une moyenne fiable.
        Renvoie une liste des temps d'exécution pour chaque taille.
        """
        times = []
        for n in n_values:
            test_func = self.wrapper(func, n)
            t = timeit.timeit(test_func, number=number)
            times.append(t)
        return times

    @staticmethod
    def fit_scale_factor(n_values, measured_times, theoretical_func):
        """
        Calcule le facteur de normalisation optimal (k) pour que k * theoretical_func(n)
        s'ajuste au mieux aux mesures (via la methode des moindres carrés)
        """
        f_vals = np.array([theoretical_func(n) for n in n_values])
        measured = np.array(measured_times)
        k = np.dot(measured, f_vals) / np.dot(f_vals, f_vals)
        return k

    @staticmethod
    def plot_benchmarks(n_values, benchmark_results, labels, generateur):
        plt.figure(figsize=(12, 7))
        plt.style.use("seaborn-v0_8-darkgrid")
        for i, (label, times) in enumerate(zip(labels, benchmark_results)):
            # Affichage réel
            plt.plot(
                n_values,
                times,
                marker="o",
                linestyle="-",
                linewidth=2,
                label=label,
                alpha=0.8,
            )

            # Courbe théorique adaptée
            mid_idx = len(n_values) // 2
            n_mid = n_values[mid_idx]
            t_mid = times[mid_idx] if mid_idx < len(times) else 1e-6

            if "énumération" in label.lower():
                # Tendance O(n·2ⁿ)
                theo = [n * (2**n) for n in n_values]
                k = t_mid / (n_mid * (2**n_mid))
                theo_times = [k * val for val in theo]
                plt.plot(
                    n_values,
                    theo_times,
                    "--",
                    label="Tendance O(n·2ⁿ)",
                    alpha=0.5,
                )

            elif "glouton" in label.lower():
                # Tendance O(n)
                theo = [n for n in n_values]
                k = t_mid / n_mid
                theo_times = [k * val for val in theo]
                plt.plot(
                    n_values,
                    theo_times,
                    "--",
                    label="Tendance O(n)",
                    alpha=0.5,
                )

        plt.xlabel("Nombre de demandes", fontsize=12)
        plt.ylabel("Temps (s)", fontsize=12)
        plt.title(f"Tendances de complexité\nDonnées: {generateur.__name__}", pad=20)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale("log")
        plt.tight_layout()
        plt.show()

    def main(self, nbr_of_demand: int):
        """
        Fonction principale qui lance le benchmark pour chaque fonction d'optimisation et trace les résultats.
        """
        # Définition des tailles de données à tester.
        n_values = list(range(1, nbr_of_demand + 1))

        labels = list(self.functions_dict.keys())
        funcs = list(self.functions_dict.values())

        # Exécute le benchmark pour chaque fonction.
        benchmark_results = [self.benchmark_function(func, n_values) for func in funcs]

        # Affiche les résultats.
        self.plot_benchmarks(n_values, benchmark_results, labels, self.generateur)


# Instanciation avec le nombre maximum de demandes à tester
tempo_bench = ComplexiteTempo(
    # Decommenter les courbes que vous voulez obtenir
    functions_dict={
        "Optimisation Glouton": optim_glouton,
        "Optimisation par énumération exhaustive": optim_enum,
    },

    # Vous pouvez changer de generateur afin de tester les comportements sur d'autres jeux de données 
    generateur=generateur_chevauchements_controle,
)
tempo_bench.main(12)

