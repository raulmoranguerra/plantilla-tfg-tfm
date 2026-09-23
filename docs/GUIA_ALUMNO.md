# Guía del alumno: puesta en marcha

Tiempo estimado: 15 minutos. Al terminar tendrás la memoria compilando
sola en cada cambio, el calendario de hitos con fechas y un tablero con
las tareas del TFG/TFM.

## 1. Crea tu repositorio

En la página de la plantilla pulsa **Use this template → Create a new repository**:

- **Owner**: tu usuario.
- **Name**: por ejemplo `tfg-apellido-tema`.
- **Visibility**: **Private** (recomendado: tu trabajo no es público hasta que lo defiendas).

> ¿Por qué *template* y no *fork*? Un fork de un repositorio público no
> puede ser privado, arrastra el historial de la plantilla y tiene las
> Actions desactivadas por defecto. Si tu director te pide un fork, funciona
> igual, pero antes de nada activa las Actions en la pestaña **Actions**.

## 2. Da acceso a tu director

**Settings → Collaborators → Add people** → el usuario de GitHub de tu director.
Si le das rol *Write*, podrá comentar, revisar y editar.

Opcional: edita `.github/CODEOWNERS` para que se le pida la revisión
automáticamente en cada pull request.

## 3. Rellena tus datos

Edita **`memoria/config/datos.tex`** (puedes hacerlo desde la web con el
lápiz ✏️): tipo de trabajo (TFG/TFM), titulación, título, autor, director,
fecha y `\NombreEntrega`. Haz *commit* en `main`.

En la pestaña **Actions** verás el workflow **Compilar**. Cuando esté en
verde ✅, tu PDF estará en **Releases → Borrador**. Ese enlace siempre
apunta a la última versión y se lo puedes pasar a tu director.

## 4. Crea el calendario y las tareas

**Actions → Inicializar proyecto → Run workflow**:

| Campo | Ejemplo |
|---|---|
| Fecha de inicio | `2026-10-01` |
| Semanas hasta la defensa | `36` (TFG de curso completo) · `24` (TFM de un cuatrimestre) |
| Crear tablero | ✅ (ver paso 5) |

El workflow crea:

- Las **etiquetas**.
- Los **8 hitos con fecha**: arranque, estado del arte, seguimiento, desarrollo, resultados, borrador, entrega y defensa.
- **24 issues** con las tareas típicas, cada una asignada a su hito.

Revisa las fechas en **Issues → Milestones** y ajústalas con tu director.
Puedes volver a ejecutar el workflow con otra fecha: no duplica nada.

## 5. (Recomendado) Tablero de GitHub Projects

El token automático de Actions no puede crear tableros, así que hace falta
un token personal una sola vez:

1. **GitHub → Settings (tu perfil) → Developer settings → Personal access tokens → Tokens (classic) → Generate new token**.
   Dale los permisos `repo` y `project` y una caducidad que cubra todo el curso.
2. En tu repositorio: **Settings → Secrets and variables → Actions → New repository secret**.
   Nombre: `PROYECTO_TOKEN`. Valor: el token.
3. Vuelve a ejecutar **Inicializar proyecto** con la casilla del tablero marcada.

Después, en el tablero (pestaña **Projects** de tu perfil), dedica un minuto a lo siguiente:

- Crea una vista **Board** agrupada por *Status* (Todo / In progress / Done).
- Crea una vista **Roadmap** por *Milestone*.
- En **Workflows**, activa *Auto-add to project* para que los issues nuevos entren solos.

## 6. Informe semanal

Cada lunes se abre un issue **«Seguimiento semanal»** con tus commits, los
issues cerrados, el progreso de cada hito y alertas. Responde en un
comentario a las tres preguntas del final (qué has hecho, qué harás, qué te
bloquea). Es tu parte de horas para el director.

Para que el informe mencione a tu director: **Settings → Secrets and
variables → Actions → Variables → New variable** con el nombre
`DIRECTOR_GITHUB` y su usuario de GitHub (sin @).

## 7. Tu entorno para escribir

Elige una opción:

- **Local (recomendado)**: instala [MacTeX](https://tug.org/mactex/), [TeX Live](https://tug.org/texlive/) o [MiKTeX](https://miktex.org/) y [VS Code](https://code.visualstudio.com/). Al abrir el repositorio, VS Code te propondrá las extensiones recomendadas (LaTeX Workshop y el corrector LTeX en español). Cada vez que guardes, compila.
  ```bash
  git clone git@github.com:<usuario>/<repo>.git && cd <repo>
  make            # o: make vigilar
  ```
- **En el navegador, sin instalar nada**: **Code → Codespaces → Create codespace on main**. Tiene TeX Live y VS Code ya preparados.
- **Overleaf**: con una cuenta que tenga sincronización con GitHub, importa el repositorio y fija `memoria/main.tex` como documento principal. Haz *pull* y *push* desde el menú de GitHub de Overleaf con frecuencia.

Para las figuras en Python:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
make figuras
```

## 8. Día a día

Lee el [flujo de trabajo](FLUJO_DE_TRABAJO.md). En resumen:

1. Coge un issue del tablero y muévelo a *In progress*.
2. Trabaja en una rama (`cap2-estado-arte`) con commits pequeños.
3. Abre un **pull request** cuando quieras revisión. La CI adjunta el PDF con tus cambios marcados.
4. Tras la revisión, *merge* a `main`. El PDF de *Releases → Borrador* se actualiza solo.
5. En cada hito importante crea una etiqueta (`v0.3-seguimiento`, `v0.9-borrador`, `v1.0-entrega`) y se publicará una versión con sus PDF.

## Problemas frecuentes

| Síntoma | Solución |
|---|---|
| La CI falla en rojo | Abre la ejecución y mira el paso **Mostrar errores de LaTeX**: indica fichero y línea. |
| `Citation … undefined` | La clave no existe en `referencias.bib` o tiene una errata. |
| `File … not found` en una figura | La ruta es relativa a `memoria/figuras/` y se escribe sin extensión. |
| Aparece un «??» en una referencia | Falta el `\label`, o no has vuelto a compilar (latexmk lo hace solo). |
| No aparece el tablero | Falta el secreto `PROYECTO_TOKEN`, o el token no tiene el permiso `project`. |
| No se abre el informe semanal | Comprueba que las Actions están activadas (en los forks vienen desactivadas). |
