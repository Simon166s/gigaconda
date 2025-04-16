import matplotlib.pyplot as plt
import timeit
import numpy as np
import generateurs_coord

class ComplexiteTempo:
    def __init__(
        self,
        functions_dict: dict = None,
        generateur= generateurs_coord.generateur_donnee,
    ):
        """Initialise l'objet avec les fonctions à évaluer et le generateur de donné choisi


        Args:
            functions_dict (dict, optional): les fonctions à tester avec leur label  . Defaults to None
            generateur (_type_, optional): la fonction générative de données. Defaults to generateur_non_chevauchant.
        """
        self.generateur = generateur
        self.functions_dict = functions_dict

    def wrapper(self, func: callable, n: int) -> callable:
        """ Génère une fonction sans argument qui exécute `func` sur un jeu de données
        généré par generateur_base_de_donnees pour une taille donnée `n`.

        Args:
            func (_type_): la fonction a wrap
            n (_type_): le nombre de donnes à generer par le générateur 

        Returns:
            _type_: la fonction wrap générée sans argument pour l'execution avec timeit
        """ """

        """
        data = self.generateur(n)
        return lambda: func(data)

    def benchmark_function(
        self, func: callable, n_values: int, number: int = 100
    ) -> list:
        """Mesure le temps d'exécution de la fonction `func` pour une liste de tailles `n_values`.
        Chaque test est répété `number` fois pour obtenir une moyenne fiable.
        Renvoie une liste des temps d'exécution pour chaque taille.

        Args:
            func (callable[list]): la fonction d'optimisation à tester
            n_values (int): le nombre valeur maximum en entré dans les données
            number (int, optional): nombre d'itération pour obtenir une moyenne fiable. Defaults to 100.

        Returns:
            list: la liste des temps d'éxécution pour chaque itération
        """
        times = []
        for n in n_values:
            test_func = self.wrapper(func, n)
            t = timeit.timeit(test_func, number=number)
            times.append(t)
        return times

    @staticmethod
    def fit_scale_factor(n_values: int, measured_times, theoretical_func):
        """ """
        f_vals = np.array([theoretical_func(n) for n in n_values])
        measured = np.array(measured_times)
        k = np.dot(measured, f_vals) / np.dot(f_vals, f_vals)
        return k

    @staticmethod
    def plot_benchmarks(
        n_values: int, benchmark_results: list, labels: str, generateur: callable
    ) -> None:
        """Affichage des courbes à partir des temps d'execution calculés, utilisation des labels
        pour afficher aussi les courbes théoriques

        Args:
            n_values (int): nombre de valeurs maximum en entré
            benchmark_results (list): temps d'execution
            labels (str): label des fonctions testées
            generateur (callable[int]): générateur utilisé pour la simulation
        """
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

            if "O(n·2ⁿ)" in label.lower():
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

            elif "O(n)" in label.lower():
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

    def main(self, nbr_of_demand: int) -> None:
        """Fonction principale qui lance le benchmark pour chaque fonction d'optimisation et trace les résultats.


        Args:
            nbr_of_demand (int): le nombre de données maximum en entré
        """
        # Définition des tailles de données à tester.
        n_values = list(range(1, nbr_of_demand + 1))

        labels = list(self.functions_dict.keys())
        funcs = list(self.functions_dict.values())

        # Exécute le benchmark pour chaque fonction.
        benchmark_results = [self.benchmark_function(func, n_values) for func in funcs]

        # Affiche les résultats.
        self.plot_benchmarks(n_values, benchmark_results, labels, self.generateur)



