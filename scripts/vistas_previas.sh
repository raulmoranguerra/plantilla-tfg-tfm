#!/usr/bin/env bash
# Mantiene la rama `vistas-previas` con los PDF de cada pull request abierto
# (carpetas pr-<N>/). GitHub muestra los PDF de una rama en su propio visor,
# así que el comentario del PR puede enlazarlos para leerlos en el navegador.
# La rama se reescribe como un único commit en cada cambio, para que los PDF
# antiguos no se acumulen en el historial del repositorio.
#
# Uso (desde la CI):  scripts/vistas_previas.sh publicar <N> <dir_pdf>
#                     scripts/vistas_previas.sh borrar <N>
# Requiere GH_TOKEN y GITHUB_REPOSITORY.
set -euo pipefail

ACCION="${1:?publicar|borrar}"
PR="${2:?número de PR}"
ORIGEN="${3:-dist}"
RAMA=vistas-previas
URL="https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
TRABAJO="$(mktemp -d)"
ORIGEN="$(cd "$ORIGEN" 2>/dev/null && pwd || echo "$ORIGEN")"

git config --global user.name "github-actions[bot]"
git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"

if git clone -q --depth 1 --branch "$RAMA" "$URL" "$TRABAJO" 2>/dev/null; then
  cd "$TRABAJO"
else
  [[ "$ACCION" == borrar ]] && { echo "No existe la rama $RAMA: nada que borrar."; exit 0; }
  git init -q "$TRABAJO" && cd "$TRABAJO" && git remote add origin "$URL"
fi

rm -rf "pr-$PR"
if [[ "$ACCION" == publicar ]]; then
  mkdir -p "pr-$PR"
  for f in "$ORIGEN"/*.pdf; do
    case "$(basename "$f")" in
      Cambios_*)                  cp "$f" "pr-$PR/cambios.pdf" ;;
      Presentacion_seguimiento_*) cp "$f" "pr-$PR/presentacion-seguimiento.pdf" ;;
      Presentacion_defensa_*)     cp "$f" "pr-$PR/presentacion-defensa.pdf" ;;
      *)                          cp "$f" "pr-$PR/memoria.pdf" ;;
    esac
  done
fi

if ! ls -d pr-* > /dev/null 2>&1; then
  git push -q origin --delete "$RAMA" 2>/dev/null || true
  echo "No quedan PR abiertos: rama $RAMA eliminada."
  exit 0
fi

cat > README.md <<'EOF'
# Vistas previas de los pull requests

Rama generada automáticamente por el workflow **Compilar**: contiene los PDF
de cada pull request abierto (`pr-<número>/`). Se reescribe en cada cambio
y se borra la carpeta al cerrar el PR. No la modifiques a mano.
EOF

git checkout -q --orphan nueva
git add -A
git commit -q -m "Vistas previas de los pull requests abiertos"
git push -q -f origin nueva:"$RAMA"
echo "Rama $RAMA actualizada (pr-$PR: $ACCION)."
