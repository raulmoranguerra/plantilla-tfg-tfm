"""Ejecuta todos los scripts de figuras de esta carpeta (make figuras)."""

import importlib
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DIR))

EXCLUIR = {"estilo", "generar_todas"}

for script in sorted(DIR.glob("*.py")):
    if script.stem in EXCLUIR:
        continue
    print(f"[{script.stem}]")
    importlib.import_module(script.stem).main()
