"""Figura y tabla de ejemplo. Cópialo como punto de partida para las tuyas."""

import numpy as np

from estilo import guardar, guardar_tabla, plt


def main():
    rng = np.random.default_rng(42)  # semilla fija: resultados reproducibles
    t = np.linspace(0, 10, 200)
    tau = 2.5
    referencia = np.exp(-t / tau)
    medida = referencia + rng.normal(0, 0.03, t.size)

    fig, ax = plt.subplots()
    ax.plot(t, medida, ".", markersize=3, alpha=0.6, label="Medida")
    ax.plot(t, referencia, label=r"Modelo $e^{-t/\tau}$")
    ax.set_xlabel(r"Tiempo (\si{\second})" if plt.rcParams["text.usetex"] else "Tiempo (s)")
    ax.set_ylabel("Amplitud normalizada")
    ax.legend()
    guardar(fig, "ejemplo_curva")

    error = medida - referencia
    guardar_tabla(
        "ejemplo_tabla",
        cabecera=["Métrica", "Valor"],
        filas=[
            ["MAE", float(np.mean(np.abs(error)))],
            ["RMSE", float(np.sqrt(np.mean(error**2)))],
            ["Error máximo", float(np.max(np.abs(error)))],
            [r"$\tau$ (s)", tau],
        ],
        titulo="Métricas de error del ejemplo (generada desde Python).",
        etiqueta="tab:ejemplo",
        decimales=3,
    )


if __name__ == "__main__":
    main()
