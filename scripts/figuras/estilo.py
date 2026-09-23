"""Estilo común para todas las figuras de la memoria.

Cada script de figura hace ``from estilo import guardar, plt`` y termina con
``guardar(fig, "nombre")``. Así todas las figuras comparten tipografía
(la de la memoria si hay LaTeX instalado), tamaños y coma decimal, y se
escriben en ``memoria/figuras/generadas/`` en PDF vectorial.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
DIR_FIGURAS = RAIZ / "memoria" / "figuras" / "generadas"
DIR_TABLAS = RAIZ / "memoria" / "tablas" / "generadas"

# Ancho útil de página en la memoria (A4, márgenes 3 + 2,5 cm) en pulgadas
ANCHO_TEXTO = 15.5 / 2.54

USA_LATEX = shutil.which("latex") is not None

plt.rcParams.update({
    "text.usetex": USA_LATEX,
    "text.latex.preamble": (
        r"\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}"
        r"\usepackage{lmodern}\usepackage{amsmath}\usepackage{siunitx}"
    ),
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman", "Computer Modern Roman", "DejaVu Serif"],
    "axes.formatter.use_locale": False,
    "axes.unicode_minus": False,
    "font.size": 10,
    "axes.titlesize": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.figsize": (ANCHO_TEXTO * 0.8, ANCHO_TEXTO * 0.5),
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.04,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "lines.linewidth": 1.4,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def num(x: float, decimales: int = 2) -> str:
    """Formatea un número con coma decimal (válido en texto y en modo math)."""
    s = f"{x:.{decimales}f}"
    return s.replace(".", "{,}") if USA_LATEX else s.replace(".", ",")


def _formateador_coma(valor, _pos):
    s = f"{valor:g}"
    return s.replace(".", "{,}") if USA_LATEX else s.replace(".", ",")


def guardar(fig, nombre: str, coma_decimal: bool = True) -> Path:
    """Guarda la figura en PDF en memoria/figuras/generadas/<nombre>.pdf."""
    if coma_decimal:
        for ax in fig.axes:
            ax.xaxis.set_major_formatter(FuncFormatter(_formateador_coma))
            ax.yaxis.set_major_formatter(FuncFormatter(_formateador_coma))
    DIR_FIGURAS.mkdir(parents=True, exist_ok=True)
    ruta = DIR_FIGURAS / f"{nombre}.pdf"
    fig.savefig(ruta, metadata={"CreationDate": None, "Creator": None})
    plt.close(fig)
    print(f"  figura -> {ruta.relative_to(RAIZ)}")
    return ruta


# El "$" no se escapa: permite escribir fórmulas LaTeX en las celdas
_ESCAPES = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}


def _celda(valor, decimales: int) -> str:
    if isinstance(valor, float):
        return rf"\num{{{valor:.{decimales}f}}}"
    texto = str(valor)
    return "".join(_ESCAPES.get(c, c) for c in texto)


def guardar_tabla(nombre: str, cabecera: list[str], filas: list[list],
                  titulo: str, etiqueta: str, decimales: int = 2,
                  alineacion: str | None = None) -> Path:
    """Escribe una tabla booktabs lista para \\input{tablas/generadas/<nombre>}.

    Los float se formatean con \\num{} (coma decimal vía siunitx). Para
    símbolos griegos usa texto LaTeX entre $...$ (p. ej. "$\\sigma$"),
    nunca caracteres Unicode como σ.
    """
    alineacion = alineacion or "l" + "c" * (len(cabecera) - 1)
    lineas = [
        r"% Generado automáticamente por scripts/figuras. NO EDITAR A MANO.",
        r"\begin{table}[H]",
        r"  \centering",
        rf"  \caption{{{titulo}}}",
        rf"  \label{{{etiqueta}}}",
        rf"  \begin{{tabular}}{{{alineacion}}}",
        r"    \toprule",
        "    " + " & ".join(cabecera) + r" \\",
        r"    \midrule",
    ]
    for fila in filas:
        lineas.append("    " + " & ".join(_celda(v, decimales) for v in fila) + r" \\")
    lineas += [r"    \bottomrule", r"  \end{tabular}", r"\end{table}", ""]
    DIR_TABLAS.mkdir(parents=True, exist_ok=True)
    ruta = DIR_TABLAS / f"{nombre}.tex"
    ruta.write_text("\n".join(lineas), encoding="utf-8")
    print(f"  tabla  -> {ruta.relative_to(RAIZ)}")
    return ruta
