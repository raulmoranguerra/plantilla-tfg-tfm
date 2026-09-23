#!/usr/bin/env python3
"""Crea en GitHub las etiquetas, hitos e issues de .github/proyecto/plan.yml
(el tablero de GitHub Projects lo crea el director con tablero.py).

Es idempotente: se puede ejecutar varias veces sin duplicar nada (si un hito
ya existe solo se actualiza su fecha; si un issue con el mismo título ya
existe, no se vuelve a crear).

Uso (normalmente desde el workflow "Inicializar proyecto"):
    python3 scripts/proyecto/inicializar.py --inicio 2026-10-01 --semanas 36

En local requiere `gh` autenticado y `pip install pyyaml`.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]


def gh(*args: str, check: bool = True) -> str:
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)}\n{r.stderr.strip()}")
    return r.stdout.strip()


def repo_actual() -> str:
    return os.environ.get("GITHUB_REPOSITORY") or gh(
        "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")


def crear_etiquetas(repo: str, etiquetas: list[dict]) -> None:
    print("== Etiquetas")
    for e in etiquetas:
        gh("label", "create", e["nombre"], "--repo", repo, "--color", e["color"],
           "--description", e.get("descripcion", ""), "--force")
        print(f"  ✓ {e['nombre']}")


def crear_hitos(repo: str, hitos: list[dict], inicio: date, semanas: int) -> None:
    print("== Hitos")
    existentes = {m["title"]: m["number"] for m in json.loads(
        gh("api", f"repos/{repo}/milestones?state=all&per_page=100"))}
    for h in hitos:
        fecha = inicio + timedelta(weeks=round(h["fraccion"] * semanas))
        campos = ["-f", f"title={h['titulo']}", "-f", f"description={h['descripcion']}",
                  "-f", f"due_on={fecha.isoformat()}T23:59:59Z"]
        if h["titulo"] in existentes:
            gh("api", "-X", "PATCH", f"repos/{repo}/milestones/{existentes[h['titulo']]}", *campos)
            print(f"  ↻ {h['titulo']} → {fecha}")
        else:
            gh("api", "-X", "POST", f"repos/{repo}/milestones", *campos)
            print(f"  ✓ {h['titulo']} → {fecha}")


def crear_issues(repo: str, issues: list[dict], asignado: str | None) -> list[str]:
    print("== Issues")
    existentes = {i["title"]: i["url"] for i in json.loads(gh(
        "issue", "list", "--repo", repo, "--state", "all", "--limit", "1000",
        "--json", "title,url"))}
    url_repo = f"https://github.com/{repo}"
    urls = []
    for i in issues:
        if i["titulo"] in existentes:
            print(f"  = {i['titulo']} (ya existe)")
            urls.append(existentes[i["titulo"]])
            continue
        cuerpo = i.get("cuerpo", "").replace("{url_repo}", url_repo)
        args = ["issue", "create", "--repo", repo, "--title", i["titulo"],
                "--body", cuerpo, "--milestone", i["hito"]]
        for e in i.get("etiquetas", []):
            args += ["--label", e]
        try:
            url = gh(*args, *(["--assignee", asignado] if asignado else []))
        except RuntimeError:
            url = gh(*args)  # p. ej. si el propietario es una organización
        urls.append(url)
        print(f"  ✓ {i['titulo']}")
    return urls


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--inicio", default=date.today().isoformat(), help="Fecha de inicio (AAAA-MM-DD)")
    p.add_argument("--semanas", type=int, default=36, help="Duración total hasta la defensa")
    p.add_argument("--sin-issues", action="store_true", help="Crear solo etiquetas e hitos")
    p.add_argument("--plan", default=str(RAIZ / ".github" / "proyecto" / "plan.yml"))
    a = p.parse_args()

    plan = yaml.safe_load(Path(a.plan).read_text(encoding="utf-8"))
    repo = repo_actual()
    if json.loads(gh("api", f"repos/{repo}"))["is_template"]:
        sys.exit("Este repositorio es la plantilla: créalo primero con 'Use this template'.")
    inicio = date.fromisoformat(a.inicio)
    print(f"Repositorio: {repo} · inicio {inicio} · {a.semanas} semanas")

    crear_etiquetas(repo, plan["etiquetas"])
    crear_hitos(repo, plan["hitos"], inicio, a.semanas)
    if not a.sin_issues:
        crear_issues(repo, plan["issues"], repo.split("/")[0])
    print("\nListo. Revisa las fechas de los hitos en la pestaña Issues → Milestones.")


if __name__ == "__main__":
    main()
