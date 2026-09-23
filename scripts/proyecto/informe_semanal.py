#!/usr/bin/env python3
"""Abre un issue "Seguimiento semanal" con la actividad de los últimos 7 días:
commits, issues cerrados, pull requests pendientes, progreso de los hitos y
alertas (inactividad, hitos vencidos, bloqueos). Menciona al director: el
de la variable DIRECTOR o, si no existe, el campo `director` de plan.yml.

Lo ejecuta cada lunes el workflow "Informe semanal". En local:
    DIRECTOR=usuario python3 scripts/proyecto/informe_semanal.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


def sh(*args: str) -> str:
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip()


def gh_json(*args: str):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    return json.loads(r.stdout or "[]") if r.returncode == 0 else []


def director_por_defecto() -> str:
    """Lee `director:` de .github/proyecto/plan.yml (sin depender de PyYAML)."""
    plan = Path(__file__).resolve().parents[2] / ".github" / "proyecto" / "plan.yml"
    m = re.search(r'^director:\s*"?([\w-]*)"?', plan.read_text(encoding="utf-8"), re.M) if plan.exists() else None
    return m.group(1) if m else ""


def barra(hechos: int, total: int, ancho: int = 10) -> str:
    if total == 0:
        return "—"
    llenos = round(ancho * hechos / total)
    return "█" * llenos + "░" * (ancho - llenos) + f" {100 * hechos // total} %"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="Imprime el informe sin crear el issue")
    p.add_argument("--dias", type=int, default=7)
    a = p.parse_args()

    repo = os.environ.get("GITHUB_REPOSITORY") or sh(
        "gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")
    if (gh_json("api", f"repos/{repo}") or {}).get("is_template"):
        print("Repositorio plantilla: no se genera informe.")
        return

    hoy = date.today()
    desde = hoy - timedelta(days=a.dias)
    alumno = repo.split("/")[0]
    director = (os.environ.get("DIRECTOR") or director_por_defecto()).lstrip("@")

    # --- Actividad en git --------------------------------------------------
    commits = sh("git", "log", f"--since={desde.isoformat()}", "--no-merges",
                 "--pretty=format:- `%h` %s _(%ad)_", "--date=format:%d/%m").splitlines()
    ultimo = sh("git", "log", "-1", "--format=%cI")
    dias_sin_commits = (datetime.now(timezone.utc) - datetime.fromisoformat(ultimo)).days
    base = sh("git", "rev-list", "-1", f"--before={desde.isoformat()}", "HEAD")
    cambios_memoria = sh("git", "diff", "--shortstat", base, "HEAD", "--", "memoria/") if base else ""

    # --- Issues, PR e hitos -----------------------------------------------
    cerrados = gh_json("issue", "list", "--repo", repo, "--state", "closed", "--limit", "100",
                       "--search", f"closed:>={desde.isoformat()} -label:seguimiento",
                       "--json", "number,title")
    abiertos = gh_json("issue", "list", "--repo", repo, "--state", "open", "--limit", "100",
                       "--search", f"created:>={desde.isoformat()} -label:seguimiento",
                       "--json", "number,title")
    bloqueos = gh_json("issue", "list", "--repo", repo, "--state", "open",
                       "--label", "bloqueo", "--json", "number,title")
    dudas = gh_json("issue", "list", "--repo", repo, "--state", "open",
                    "--label", "duda", "--json", "number,title")
    prs = gh_json("pr", "list", "--repo", repo, "--state", "open",
                  "--json", "number,title,isDraft,createdAt")
    hitos = gh_json("api", f"repos/{repo}/milestones?state=open&sort=due_on&direction=asc")

    # --- Alertas ------------------------------------------------------------
    alertas = []
    if dias_sin_commits >= 14:
        alertas.append(f"⚠️ **{dias_sin_commits} días sin commits.**")
    for h in hitos:
        if h.get("due_on") and date.fromisoformat(h["due_on"][:10]) < hoy and h["open_issues"]:
            alertas.append(f"⏰ Hito vencido: **{h['title']}** ({h['open_issues']} issues abiertos).")
    if bloqueos:
        alertas.append(f"🛑 {len(bloqueos)} bloqueo(s) abiertos.")
    for pr in prs:
        dias = (datetime.now(timezone.utc) - datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))).days
        if not pr["isDraft"] and dias >= 7:
            alertas.append(f"👀 PR #{pr['number']} lleva {dias} días esperando revisión.")

    # --- Informe -------------------------------------------------------------
    L = []
    if director:
        L.append(f"@{director} · @{alumno}\n")
    L.append("### Alertas\n" + ("\n".join(f"- {x}" for x in alertas) if alertas else "Ninguna ✅"))
    L.append(f"\n### Actividad (últimos {a.dias} días)")
    L.append(f"- **{len(commits)} commits**" + (f" · memoria: {cambios_memoria}" if cambios_memoria else ""))
    L.append(f"- **{len(cerrados)} issues cerrados**, {len(abiertos)} nuevos")
    if cerrados:
        L.append("\n<details><summary>Issues cerrados</summary>\n")
        L += [f"- #{i['number']} {i['title']}" for i in cerrados]
        L.append("\n</details>")
    if commits:
        L.append("\n<details><summary>Commits</summary>\n")
        L += commits[:50]
        L.append("\n</details>")

    L.append("\n### Hitos\n| Hito | Fecha | Progreso |\n|---|---|---|")
    for h in hitos:
        fecha = h["due_on"][:10] if h.get("due_on") else "—"
        total = h["open_issues"] + h["closed_issues"]
        L.append(f"| [{h['title']}]({h['html_url']}) | {fecha} | {barra(h['closed_issues'], total)} |")

    if prs or bloqueos or dudas:
        L.append("\n### Pendiente de revisión o respuesta")
        L += [f"- PR #{x['number']} {x['title']}{' (borrador)' if x['isDraft'] else ''}" for x in prs]
        L += [f"- 🛑 #{x['number']} {x['title']}" for x in bloqueos]
        L += [f"- ❓ #{x['number']} {x['title']}" for x in dudas]

    L.append(f"""
### Para el alumno (responder en un comentario)
1. ¿Qué he hecho esta semana?
2. ¿Qué voy a hacer la próxima?
3. ¿Tengo algún bloqueo o duda?

<sub>Generado automáticamente por el workflow «Informe semanal» el {hoy:%d/%m/%Y}.</sub>""")
    cuerpo = "\n".join(L)
    titulo = f"Seguimiento semanal · {desde:%d/%m} – {hoy:%d/%m/%Y}"

    if a.dry_run:
        print(f"# {titulo}\n\n{cuerpo}")
        return

    sh("gh", "label", "create", "seguimiento", "--repo", repo, "--color", "bfdadc",
       "--description", "Informe semanal automático", "--force")
    anteriores = gh_json("issue", "list", "--repo", repo, "--state", "open",
                         "--label", "seguimiento", "--json", "number")
    url = sh("gh", "issue", "create", "--repo", repo, "--title", titulo,
             "--body", cuerpo, "--label", "seguimiento")
    print(url)
    for i in anteriores:
        sh("gh", "issue", "close", str(i["number"]), "--repo", repo,
           "--comment", f"Sustituido por el informe de esta semana: {url}")


if __name__ == "__main__":
    main()
