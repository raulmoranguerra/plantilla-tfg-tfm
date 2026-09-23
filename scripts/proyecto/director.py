#!/usr/bin/env python3
"""Herramienta del director: alta de alumnos, tableros y seguimiento.

GitHub no deja crear tableros desde Actions sin un token personal, así que
los crea el director con su propio `gh` (una vez: `gh auth refresh -s project`).
Cada tablero vive en la cuenta del director, contiene los issues del
repositorio del alumno y se comparte con el alumno como editor.

    # Alta de un alumno: hitos + issues en su repo y tablero compartido
    python3 scripts/proyecto/director.py alta alumno/tfg-repo --inicio 2026-10-01 --semanas 36

    # Estado de todos tus alumnos (y añade sus issues nuevos a los tableros)
    python3 scripts/proyecto/director.py seguimiento

    # Solo sincronizar los tableros
    python3 scripts/proyecto/director.py sincronizar

Si en tu cuenta existe un tablero llamado «Plantilla tablero TFG», cada
tablero nuevo se crea como copia suya (con sus vistas, campos y
automatizaciones). Así solo hay que configurar las vistas una vez.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inicializar import gh  # noqa: E402

PLANTILLA = "Plantilla tablero TFG"
MARCA = "Seguimiento del repositorio "


def usuario_actual() -> str:
    return gh("api", "user", "--jq", ".login")


def proyectos(propietario: str) -> list[dict]:
    datos = json.loads(gh("project", "list", "--owner", propietario,
                          "--format", "json", "--limit", "200"))
    return datos["projects"]


def asegurar_tablero(repo: str, propietario: str) -> dict:
    """Devuelve el tablero del repo en la cuenta del director (lo crea si no existe)."""
    titulo = f"{repo.split('/')[1]} · seguimiento"
    existentes = proyectos(propietario)
    for p in existentes:
        if (p.get("shortDescription") or "").endswith(MARCA + repo) or p["title"] == titulo:
            print(f"  = Tablero existente: {p['url']}")
            if not (p.get("shortDescription") or "").endswith(MARCA + repo):
                gh("project", "edit", str(p["number"]), "--owner", propietario,
                   "--description", MARCA + repo)
            return p
    plantilla = next((p for p in existentes if p["title"] == PLANTILLA), None)
    if plantilla:
        p = json.loads(gh("project", "copy", str(plantilla["number"]), "--source-owner", propietario,
                          "--target-owner", propietario, "--title", titulo, "--format", "json"))
        print(f"  ✓ Tablero copiado de «{PLANTILLA}»: {p['url']}")
    else:
        p = json.loads(gh("project", "create", "--owner", propietario, "--title", titulo,
                          "--format", "json"))
        print(f"  ✓ Tablero creado: {p['url']}")
        print(f"    Consejo: crea un tablero «{PLANTILLA}» con tus vistas (Board, Roadmap…)\n"
              "    y los siguientes se copiarán de él ya configurados.")
    gh("project", "edit", str(p["number"]), "--owner", propietario,
       "--description", MARCA + repo)
    return p


def compartir(proyecto: dict, alumno: str, propietario: str) -> None:
    if alumno.lower() == propietario.lower():
        return
    id_proyecto = proyecto.get("id") or gh(
        "project", "view", str(proyecto["number"]), "--owner", propietario,
        "--format", "json", "--jq", ".id")
    id_alumno = gh("api", f"users/{alumno}", "--jq", ".node_id")
    gh("api", "graphql", "-f", "query=mutation($p:ID!,$u:ID!){updateProjectV2Collaborators("
       "input:{projectId:$p,collaborators:[{userId:$u,role:WRITER}]}){clientMutationId}}",
       "-f", f"p={id_proyecto}", "-f", f"u={id_alumno}")
    print(f"  ✓ Compartido con @{alumno} (puede editar)")


def enlazar(proyecto: dict, repo: str, propietario: str) -> None:
    # GitHub solo permite enlazar tableros y repositorios del mismo propietario
    if repo.split("/")[0].lower() == propietario.lower():
        gh("project", "link", str(proyecto["number"]), "--owner", propietario, "--repo", repo,
           check=False)


def gh_reintentos(*args: str, intentos: int = 4) -> str:
    """gh con reintentos: la API de Projects falla a veces de forma transitoria."""
    for i in range(intentos):
        try:
            return gh(*args)
        except RuntimeError:
            if i == intentos - 1:
                raise
            time.sleep(2 * (i + 1))
    return ""


def issues_fuera_del_tablero(repo: str, numero: int, propietario: str) -> list[str]:
    """IDs de los issues del repo que aún no están en el tablero (una consulta por cada 100)."""
    duenyo, nombre = repo.split("/")
    consulta = ("query($o:String!,$n:String!,$c:String){repository(owner:$o,name:$n){"
                "issues(first:100,after:$c){pageInfo{hasNextPage endCursor}"
                "nodes{id projectItems(first:20){nodes{project{number owner{"
                "... on User{login} ... on Organization{login}}}}}}}}}")
    faltan, cursor = [], None
    while True:
        args = ["api", "graphql", "-f", f"query={consulta}", "-f", f"o={duenyo}", "-f", f"n={nombre}"]
        if cursor:
            args += ["-f", f"c={cursor}"]
        datos = json.loads(gh_reintentos(*args))["data"]["repository"]["issues"]
        for issue in datos["nodes"]:
            if not any(it["project"]["number"] == numero
                       and it["project"]["owner"]["login"].lower() == propietario.lower()
                       for it in issue["projectItems"]["nodes"]):
                faltan.append(issue["id"])
        if not datos["pageInfo"]["hasNextPage"]:
            return faltan
        cursor = datos["pageInfo"]["endCursor"]


def anadir_issues(proyecto: dict, repo: str, propietario: str) -> int:
    """Añade al tablero los issues del repo que falten. Devuelve cuántos ha añadido."""
    id_proyecto = proyecto.get("id") or gh_reintentos(
        "project", "view", str(proyecto["number"]), "--owner", propietario,
        "--format", "json", "--jq", ".id")
    faltan = issues_fuera_del_tablero(repo, proyecto["number"], propietario)
    for id_issue in faltan:
        gh_reintentos("api", "graphql", "-f",
                      "query=mutation($p:ID!,$c:ID!){addProjectV2ItemById("
                      "input:{projectId:$p,contentId:$c}){item{id}}}",
                      "-f", f"p={id_proyecto}", "-f", f"c={id_issue}")
    return len(faltan)


def alta(a) -> None:
    propietario = usuario_actual()
    alumno = a.repo.split("/")[0]
    print(f"Alta de {a.repo} (director: @{propietario})")
    cmd = [sys.executable, str(Path(__file__).with_name("inicializar.py")),
           "--inicio", a.inicio, "--semanas", str(a.semanas)]
    subprocess.run(cmd, check=True, env={**__import__("os").environ, "GITHUB_REPOSITORY": a.repo})
    print("== Tablero")
    p = asegurar_tablero(a.repo, propietario)
    enlazar(p, a.repo, propietario)
    compartir(p, alumno, propietario)
    print(f"  ✓ {anadir_issues(p, a.repo, propietario)} issues añadidos al tablero")
    print(f"\nListo: {p['url']}")


def alumnos(propietario: str) -> list[tuple[str, dict]]:
    """(repo, tablero) de cada alumno dado de alta."""
    res = []
    for p in proyectos(propietario):
        m = re.search(re.escape(MARCA) + r"(\S+/\S+)$", p.get("shortDescription") or "")
        if m:
            res.append((m.group(1), p))
    return sorted(res)


def sincronizar(_a) -> None:
    propietario = usuario_actual()
    for repo, p in alumnos(propietario):
        try:
            n = anadir_issues(p, repo, propietario)
            print(f"✓ {repo}: {n} issues nuevos añadidos → {p['url']}")
        except RuntimeError as e:
            print(f"✗ {repo}: {e}")


def _json(*args: str):
    try:
        return json.loads(gh_reintentos(*args) or "null")
    except RuntimeError:
        return None


def estado(repo: str) -> dict:
    hoy = date.today()
    commits = _json("api", f"repos/{repo}/commits?per_page=1") or []
    ultimo = (datetime.fromisoformat(commits[0]["commit"]["committer"]["date"].replace("Z", "+00:00"))
              if commits else None)
    dias = (datetime.now(timezone.utc) - ultimo).days if ultimo else None
    hitos = _json("api", f"repos/{repo}/milestones?state=open&sort=due_on&direction=asc") or []
    hito = hitos[0] if hitos else None
    vencidos = [h for h in hitos if h.get("due_on") and date.fromisoformat(h["due_on"][:10]) < hoy]
    contar = lambda *f: len(_json("issue", "list", "--repo", repo, "--state", "open",
                                  "--json", "number", *f) or [])
    prs = [x for x in (_json("pr", "list", "--repo", repo, "--json", "isDraft") or []) if not x["isDraft"]]
    versiones = [r["tagName"] for r in (_json("release", "list", "--repo", repo, "--json", "tagName",
                                              "--limit", "20") or []) if r["tagName"] != "borrador"]
    return {
        "dias": dias,
        "hito": hito,
        "vencidos": vencidos,
        "bloqueos": contar("--label", "bloqueo"),
        "dudas": contar("--label", "duda"),
        "prs": len(prs),
        "version": versiones[0] if versiones else "—",
    }


def seguimiento(a) -> None:
    propietario = usuario_actual()
    lista = alumnos(propietario)
    if not lista:
        print("No hay alumnos dados de alta. Usa: director.py alta <usuario/repo> --inicio AAAA-MM-DD")
        return
    if not a.sin_sincronizar:
        for repo, p in lista:
            try:
                anadir_issues(p, repo, propietario)
            except RuntimeError as e:
                print(f"(no se pudo sincronizar el tablero de {repo}: {e.args[0].splitlines()[-1]})")
    print(f"Seguimiento a {date.today():%d/%m/%Y}\n")
    print(f"{'Alumno':<34} {'Últ. commit':>11}  {'Hito actual':<38} {'Prog.':>5}  "
          f"{'Bloq.':>5} {'Dudas':>5} {'PR':>3}  Versión")
    for repo, p in lista:
        e = estado(repo)
        h = e["hito"]
        if h:
            total = h["open_issues"] + h["closed_issues"]
            prog = f"{100 * h['closed_issues'] // total}%" if total else "—"
            nombre = f"{h['title']} ({h['due_on'][8:10]}/{h['due_on'][5:7]})" if h.get("due_on") else h["title"]
        else:
            prog, nombre = "—", "(sin hitos abiertos)"
        dias = "—" if e["dias"] is None else f"hace {e['dias']} d"
        alertas = []
        if e["dias"] is not None and e["dias"] >= 14:
            alertas.append(f"⚠️  {e['dias']} días sin commits")
        if e["vencidos"]:
            alertas.append("⏰ vencido: " + ", ".join(x["title"] for x in e["vencidos"]))
        if e["bloqueos"]:
            alertas.append(f"🛑 {e['bloqueos']} bloqueo(s)")
        print(f"{repo:<34} {dias:>11}  {nombre[:38]:<38} {prog:>5}  "
              f"{e['bloqueos']:>5} {e['dudas']:>5} {e['prs']:>3}  {e['version']}")
        for x in alertas:
            print(f"{'':<36}{x}")
        print(f"{'':<36}{p['url']}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="orden", required=True)
    a = sub.add_parser("alta", help="Preparar el repositorio y el tablero de un alumno")
    a.add_argument("repo", help="Repositorio del alumno (usuario/repo)")
    a.add_argument("--inicio", required=True, help="Fecha de inicio (AAAA-MM-DD)")
    a.add_argument("--semanas", type=int, default=36, help="Semanas hasta la defensa")
    a.set_defaults(func=alta)
    s = sub.add_parser("sincronizar", help="Añadir los issues nuevos a todos los tableros")
    s.set_defaults(func=sincronizar)
    g = sub.add_parser("seguimiento", help="Estado de todos tus alumnos (y sincroniza tableros)")
    g.add_argument("--sin-sincronizar", action="store_true", help="No actualizar los tableros")
    g.set_defaults(func=seguimiento)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
