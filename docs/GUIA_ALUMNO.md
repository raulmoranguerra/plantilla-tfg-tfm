# Guía del alumno: puesta en marcha

Tiempo estimado: 10 minutos. Solo tienes que crear tu repositorio, invitar a
tu director y rellenar tus datos. El calendario de hitos, las tareas y el
tablero los prepara tu director.

## 1. Crea tu repositorio

En la página de la plantilla pulsa **Use this template → Create a new repository**:

- **Owner**: tu usuario.
- **Name**: por ejemplo `tfg-apellido-tema`.
- **Visibility**: **Private** (recomendado: tu trabajo no es público hasta que lo defiendas).

> ¿Por qué *template* y no *fork*? Un fork de un repositorio público no
> puede ser privado, arrastra el historial de la plantilla y tiene las
> Actions desactivadas por defecto. Si tu director te pide un fork, funciona
> igual, pero antes de nada activa las Actions en la pestaña **Actions**.

## 2. Invita a tu director

**Settings → Collaborators → Add people** → el usuario de GitHub de tu
director, con rol **Write**. Pásale también el nombre de tu repositorio
(`usuario/repo`).

Con eso, tu director ejecuta un comando que:

- Crea los **8 hitos con fecha**: arranque, estado del arte, seguimiento, desarrollo, resultados, borrador, entrega y defensa.
- Crea las **etiquetas** y **24 issues** con las tareas típicas.
- Crea un **tablero** (GitHub Projects) con todas ellas y lo comparte contigo. Te llegará una invitación por correo.

## 3. Rellena tus datos

Edita **`memoria/config/datos.tex`** (puedes hacerlo desde la web con el
lápiz ✏️): tipo de trabajo (TFG/TFM), titulación, título, autor, director,
fecha y `\NombreEntrega`. Haz *commit* en `main`.

En la pestaña **Actions** verás el workflow **Compilar**. Cuando esté en
verde ✅, tu PDF estará en **Releases → Borrador**. Ese enlace siempre
apunta a la última versión.

## 4. El tablero

Cuando tu director lo haya creado, lo verás en **tu perfil → Projects**, o en
el enlace que te pase. Úsalo para mover las tareas entre *Todo*, *In
progress* y *Done*. Los issues nuevos que abras en tu repositorio se añaden
al tablero cuando tu director actualiza el seguimiento.

> ¿Tu director te ha pedido que lo hagas tú? **Actions → Inicializar proyecto
> → Run workflow**, con la fecha de inicio y las semanas hasta la defensa
> (TFG ≈ 36, TFM ≈ 24), crea los hitos, las etiquetas y los issues. El tablero
> lo sigue creando él.

## 5. Informe semanal

Cada lunes se abre un issue **«Seguimiento semanal»** con tus commits, los
issues cerrados, el progreso de cada hito y alertas. Responde en un
comentario a las tres preguntas del final (qué has hecho, qué harás, qué te
bloquea). Es tu parte de horas para el director.

## 6. Tu entorno para escribir

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

## 7. Día a día

Lee el [flujo de trabajo](FLUJO_DE_TRABAJO.md). En resumen:

1. Coge un issue del tablero y muévelo a *In progress*.
2. Trabaja en una rama (`cap2-estado-arte`) con commits pequeños.
3. Abre un **pull request** cuando quieras revisión. La CI comenta con enlaces a la memoria y a un PDF con tus cambios marcados.
4. Tras la revisión, *merge* a `main`. El PDF de *Releases → Borrador* se actualiza solo.
5. En cada hito importante crea una etiqueta (`v0.3-seguimiento`, `v0.9-borrador`, `v1.0-entrega`) y se publicará una versión con sus PDF.

## Problemas frecuentes

| Síntoma | Solución |
|---|---|
| La CI falla en rojo | Abre la ejecución y mira el paso **Mostrar errores de LaTeX**: indica fichero y línea. |
| `Citation … undefined` | La clave no existe en `referencias.bib` o tiene una errata. |
| `File … not found` en una figura | La ruta es relativa a `memoria/figuras/` y se escribe sin extensión. |
| Aparece un «??» en una referencia | Falta el `\label`, o no has vuelto a compilar (latexmk lo hace solo). |
| No veo el tablero | Acepta la invitación que te llega por correo, o pídele el enlace a tu director. |
| No se abre el informe semanal | Comprueba que las Actions están activadas (en los forks vienen desactivadas). |
