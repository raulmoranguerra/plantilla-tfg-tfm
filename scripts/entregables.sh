#!/usr/bin/env bash
# Copia los PDF compilados a dist/ con los nombres que exige la entrega,
# a partir de \NombreEntrega (memoria/config/datos.tex).
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

NOMBRE=$(sed -n 's/^\\newcommand{\\NombreEntrega}{\(.*\)}.*/\1/p' memoria/config/datos.tex)
NOMBRE=${NOMBRE:-Memoria}
SUFIJO=${NOMBRE#*_}   # Apellido1Apellido2_Nombre

mkdir -p dist
copiar() { [[ -f "$1" ]] && cp "$1" "dist/$2" && echo "  $1 -> dist/$2" || true; }
copiar memoria/main.pdf                 "${NOMBRE}.pdf"
copiar memoria/diff.pdf                 "Cambios_${NOMBRE}.pdf"
copiar presentacion/seguimiento.pdf     "Presentacion_seguimiento_${SUFIJO}.pdf"
copiar presentacion/defensa.pdf         "Presentacion_defensa_${SUFIJO}.pdf"
