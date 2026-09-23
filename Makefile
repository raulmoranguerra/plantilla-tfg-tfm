# Atajos de compilación. Los mismos objetivos los usa la CI de GitHub.
#   make            -> memoria + presentaciones
#   make vigilar    -> recompila la memoria cada vez que guardas
#   make diff REV=v0.2-seguimiento   -> PDF con los cambios desde esa versión
#
# Para el director (requiere `gh auth refresh -s project` una vez):
#   make alta REPO=alumno/repo INICIO=2026-10-01 [SEMANAS=36]  -> hitos, issues y tablero
#   make seguimiento                                           -> estado de todos tus alumnos

SHELL   := /bin/bash
REV     ?= HEAD~1
SEMANAS ?= 36

.PHONY: all memoria presentacion vigilar figuras diff estadisticas entregables alta seguimiento limpiar ayuda

all: memoria presentacion

memoria:
	cd memoria && latexmk main.tex

presentacion:
	cd presentacion && latexmk -r ../memoria/.latexmkrc seguimiento.tex defensa.tex

vigilar:
	cd memoria && latexmk -pvc main.tex

figuras:
	python3 scripts/figuras/generar_todas.py

diff:
	scripts/latexdiff.sh $(REV)

estadisticas:
	@scripts/estadisticas.sh

entregables:
	scripts/entregables.sh

alta:
	python3 scripts/proyecto/director.py alta $(REPO) --inicio $(INICIO) --semanas $(SEMANAS)

seguimiento:
	python3 scripts/proyecto/director.py seguimiento

limpiar:
	cd memoria && latexmk -C main.tex && rm -f diff.*
	cd presentacion && latexmk -C seguimiento.tex defensa.tex
	rm -rf dist .diff-base

ayuda:
	@grep -E '^#' Makefile | sed 's/^# \{0,1\}//'
