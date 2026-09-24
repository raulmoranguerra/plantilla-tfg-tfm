# Flujo de trabajo

## Ramas y pull requests

- `main` siempre compila. Es la versión que ve el director en *Releases → Borrador*.
- Trabaja cada tarea en una rama con un nombre descriptivo: `cap2-estado-arte`, `figuras-resultados`, `correcciones-cap4`.
- Abre un **pull request** (PR) cuando quieras revisión. Si aún no está listo, ábrelo como *Draft*. Escribe `Cierra #12` en la descripción para cerrar el issue al hacer *merge*.
- La CI compila el PR y comenta con estadísticas y enlaces para ver en el navegador la memoria y un **PDF con los cambios marcados**. Revísalo tú antes que el director.
- Tras la aprobación: **Squash and merge** y borra la rama.

Para cambios pequeños (una errata, un dato) puedes hacer commit directo en `main`.

```bash
git switch -c cap2-estado-arte
# … editar …
git add -A && git commit -m "Añadir comparativa de métodos al estado del arte"
git push -u origin cap2-estado-arte
gh pr create --fill      # o desde la web
```

## Commits

- **Pequeños y frecuentes**: al menos uno por sesión de trabajo. El historial es tu copia de seguridad.
- Mensaje en **español e imperativo**, con mayúscula inicial y sin punto final: «Añadir …», «Corregir …», «Reescribir …».
- Si toca solo una parte, puedes indicarlo con un prefijo: «Cap. 3: justificar la elección del sensor».
- No subas PDF compilados ni ficheros auxiliares: el `.gitignore` ya los excluye. Las figuras en PDF sí se suben.
- En LaTeX, escribe **una frase por línea**: los diffs y las revisiones son mucho más legibles.

## Issues y tablero

- Una tarea = un issue, con su hito y sus etiquetas.
- Para dudas al director, usa la plantilla **Duda o bloqueo**. Tras cada reunión, abre un **Acta de reunión** con las decisiones y los próximos pasos.
- Registra los experimentos con la plantilla **Experimento**: hipótesis, método (commit, semilla, datos), resultado y conclusión. Te servirá para escribir el capítulo de resultados.
- Mueve las tarjetas del tablero: *Todo → In progress → Done* (el issue se cierra al hacer *merge* del PR).

## Versiones (etiquetas)

```bash
git switch main && git pull
git tag -a v0.9-borrador -m "Borrador completo para revisión"
git push origin v0.9-borrador
```

La CI publica una *release* con:

- la memoria como `TFG_Apellidos_Nombre.pdf`;
- las presentaciones;
- el PDF de cambios respecto a la etiqueta anterior.

Consulta la tabla de etiquetas en la [guía del director](GUIA_DIRECTOR.md#versiones).

## Datos y código del trabajo

- El código del desarrollo puede vivir en este mismo repositorio, en carpetas propias (`codigo/`, `firmware/`, `hardware/`…) con su propio README.
- **No subas datasets grandes**. Documenta su origen (DOI) y añade un script que los descargue en `datos/`, que está ignorado por git.
- Para ficheros binarios grandes que sí deban versionarse (modelos entrenados, por ejemplo), usa Git LFS (ver `.gitattributes`).
- Fija versiones (`requirements.txt`) y semillas para que los resultados sean reproducibles.
