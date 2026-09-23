# Atajos de compilación. Los mismos objetivos los usa la CI de GitHub.
#   make            -> memoria + presentaciones
#   make vigilar    -> recompila la memoria cada vez que guardas
#   make diff REV=v0.2-seguimiento   -> PDF con los cambios desde esa versión

SHELL := /bin/bash
REV   ?= HEAD~1

.PHONY: all memoria presentacion vigilar figuras diff estadisticas entregables limpiar ayuda

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

limpiar:
	cd memoria && latexmk -C main.tex && rm -f diff.*
	cd presentacion && latexmk -C seguimiento.tex defensa.tex
	rm -rf dist .diff-base

ayuda:
	@grep -E '^#' Makefile | sed 's/^# \{0,1\}//'
