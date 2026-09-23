#!/usr/bin/env bash
# Resumen del estado de la memoria en Markdown (lo usa la CI para el
# resumen de cada compilación y los comentarios en los pull requests).
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)/memoria"

paginas=$(grep -ao 'Output written on main.pdf ([0-9]* pages' main.log 2>/dev/null | grep -o '[0-9]*' | tail -1)
palabras=$(texcount -inc -sum -1 -utf8 -q main.tex 2>/dev/null | tail -1)
pendientes=$(grep -rho '\\pendiente{' capitulos preliminares anexos 2>/dev/null | wc -l | tr -d ' ')
notas=$(grep -rho '\\nota{' capitulos preliminares anexos 2>/dev/null | wc -l | tr -d ' ')
referencias=$(grep -c '^@' bibliografia/*.bib 2>/dev/null | awk -F: '{s+=$NF} END {print s+0}')
citadas=$(grep -ho '\\abx@aux@cite{0}{[^}]*}' main.aux 2>/dev/null | sort -u | wc -l | tr -d ' ')
avisos=$(grep -cE 'Warning|Overfull|Underfull' main.log 2>/dev/null; true)
indefinidas=$(grep -cE "(Reference|Citation) .* undefined" main.log 2>/dev/null; true)

cat <<MD
| Métrica | Valor |
|---|---|
| Páginas | ${paginas:-?} |
| Palabras (texcount) | ${palabras:-?} |
| \`\\pendiente{}\` abiertos | ${pendientes} |
| \`\\nota{}\` abiertas | ${notas} |
| Entradas en la bibliografía / citadas | ${referencias} / ${citadas} |
| Avisos de LaTeX | ${avisos:-?} |
| Referencias o citas sin definir | ${indefinidas:-?} |
MD
