#!/usr/bin/env bash
# Genera memoria/diff.pdf: la memoria actual con los cambios desde REV
# marcados (texto nuevo en azul subrayado, eliminado en rojo tachado).
# REV puede ser una etiqueta (v0.2-seguimiento), una rama o un commit.
# Uso: scripts/latexdiff.sh <REV>        (o: make diff REV=<REV>)
set -euo pipefail

REV="${1:?Uso: scripts/latexdiff.sh <etiqueta|rama|commit>}"
RAIZ="$(git rev-parse --show-toplevel)"
BASE="$RAIZ/.diff-base"

cd "$RAIZ"
rm -rf "$BASE"
git worktree prune
git worktree add --detach --quiet "$BASE" "$REV"
trap 'git -C "$RAIZ" worktree remove --force "$BASE" >/dev/null 2>&1 || rm -rf "$BASE"' EXIT

# Cada versión se "aplana" (\input/\include resueltos) desde su propio
# directorio; latexdiff --flatten resolvería ambas contra el directorio actual.
(cd "$BASE/memoria" && latexpand main.tex > "$BASE/antigua.tex")
cd memoria
latexpand main.tex > "$BASE/nueva.tex"
latexdiff --math-markup=whole "$BASE/antigua.tex" "$BASE/nueva.tex" > diff.tex
latexmk diff.tex
echo "PDF de cambios: memoria/diff.pdf (respecto a $REV)"
