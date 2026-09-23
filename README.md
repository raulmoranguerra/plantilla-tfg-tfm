# Plantilla de TFG / TFM en LaTeX

[![Compilar](../../actions/workflows/compilar.yml/badge.svg)](../../actions/workflows/compilar.yml)
[![Último PDF](https://img.shields.io/badge/PDF-última%20versión-blue)](../../releases/tag/borrador)

Plantilla completa para escribir un **Trabajo Fin de Grado o Máster** en LaTeX
con compilación automática y seguimiento del proyecto en GitHub. Viene
configurada para la **ETS de Ingeniería – ICAI (Universidad Pontificia
Comillas)** y todo lo específico de la escuela está en un solo fichero.

> **¿Eres alumno?** Empieza por la [guía del alumno](docs/GUIA_ALUMNO.md): en unos 15 minutos lo tendrás todo funcionando.
> **¿Diriges el trabajo?** Lee la [guía del director](docs/GUIA_DIRECTOR.md).

## Qué incluye

| | |
|---|---|
| 📄 **Memoria** | Clase `book` en español: portada, Anexo I firmado entre las portadas, resumen y abstract con el formato de la escuela, índices, acrónimos, bibliografía con biblatex y anexos de presupuesto y ODS. |
| 🎞️ **Presentaciones** | Beamer para el seguimiento y la defensa, con los mismos datos y figuras que la memoria. |
| 📊 **Figuras desde código** | Estilo común de matplotlib (tipografía de la memoria y coma decimal) y tablas LaTeX generadas desde Python. |
| ⚙️ **CI/CD** | Cada *push* compila en GitHub Actions. Cada PR recibe un **PDF con los cambios marcados** y un comentario con estadísticas. Cada etiqueta `v*` publica los PDF de entrega en *Releases*. |
| 📋 **Gestión del proyecto** | Con un comando (`make alta`), el director crea en el repositorio del alumno los hitos con fechas, las etiquetas y 24 issues iniciales, y un tablero de GitHub Projects compartido con él. `make seguimiento` muestra el estado de todos sus alumnos, y cada lunes se abre un **informe semanal** en cada repositorio. |
| 🧰 **Entorno** | `Makefile`, `latexmk`, VS Code (LaTeX Workshop + corrector LTeX) y Codespaces con TeX Live preinstalado. |

## Uso rápido

```bash
make              # memoria + presentaciones
make vigilar      # recompila la memoria al guardar
make figuras      # regenera figuras y tablas desde scripts/figuras/
make diff REV=v0.3-seguimiento   # PDF con los cambios desde esa versión
make estadisticas # páginas, palabras, \pendiente{} abiertos…
make limpiar

# Director
make alta REPO=alumno/repo INICIO=2026-10-01   # hitos, issues y tablero
make seguimiento                                # panel de todos los alumnos
```

Requisitos locales: TeX Live 2023 o posterior (o MacTeX / MiKTeX) con `latexmk` y `biber`. Para las figuras, Python 3.10 o posterior y `pip install -r scripts/requirements.txt`.

## Estructura

```
memoria/
  main.tex                 documento principal
  config/datos.tex         ← título, autor, director, titulación… (EDITAR PRIMERO)
  config/preambulo.tex     paquetes y formato
  config/macros.tex        comandos propios (\pendiente, \nota…)
  preliminares/            portada, agradecimientos, resumen, abstract, acrónimos
  capitulos/               un fichero por capítulo
  anexos/                  presupuesto, ODS, código
  figuras/                 figuras (generadas/ = salida de los scripts)
  tablas/generadas/        tablas generadas desde Python
  bibliografia/referencias.bib
  administrativo/          Anexo I firmado
presentacion/              seguimiento.tex, defensa.tex, estilo.tex
scripts/
  figuras/                 estilo.py + un script por figura
  proyecto/                director.py (alta, tablero, seguimiento) e informe semanal
.github/
  workflows/               compilar, inicializar-proyecto, informe-semanal
  proyecto/plan.yml        hitos, etiquetas e issues iniciales
  ISSUE_TEMPLATE/          tarea, duda, acta de reunión, experimento, compilación
docs/                      guías y checklist de entrega
```

## Documentación

- [Guía del alumno](docs/GUIA_ALUMNO.md): puesta en marcha paso a paso
- [Guía del director](docs/GUIA_DIRECTOR.md): preparar la plantilla y hacer el seguimiento
- [Flujo de trabajo](docs/FLUJO_DE_TRABAJO.md): ramas, commits, pull requests y versiones
- [Guía de estilo](docs/GUIA_ESTILO.md): convenciones de escritura en LaTeX
- [Entregables](docs/ENTREGABLES.md): checklist para el depósito y la defensa

## Licencia

La plantilla se distribuye con licencia [MIT](LICENSE). El contenido de cada memoria pertenece a su autor. El logotipo pertenece a la Universidad Pontificia Comillas.
