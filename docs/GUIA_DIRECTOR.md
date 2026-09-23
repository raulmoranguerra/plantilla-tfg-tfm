# Guía del director

## Preparar la plantilla (una vez)

1. Sube este repositorio a GitHub (a tu cuenta o a una organización del grupo).
2. **Settings → General → Template repository ✅**. Así los alumnos verán el botón *Use this template*.
3. Adapta a tu grupo, si quieres:
   - `memoria/config/datos.tex`: titulación, escuela y logo por defecto.
   - `.github/proyecto/plan.yml`: hitos (con su posición relativa en el calendario), etiquetas y tareas iniciales. Por ejemplo, añade la tarea «Entregar el informe de seguimiento a la plataforma» o elimina el Anexo I si no aplica.
   - `memoria/capitulos/`: la estructura de capítulos que prefieras.
4. Comprueba que el workflow **Compilar** está en verde en la plantilla.

> En la propia plantilla, los workflows de inicialización e informe
> semanal detectan que es una plantilla y no hacen nada.

## Cuando un alumno empieza

Pídele que siga la [guía del alumno](GUIA_ALUMNO.md) y comprueba:

- [ ] Te ha añadido como colaborador (acepta la invitación que te llega por correo).
- [ ] La compilación está en verde y existe la release **Borrador**.
- [ ] Ha ejecutado **Inicializar proyecto** y las fechas de los hitos son realistas.
- [ ] Ha definido la variable `DIRECTOR_GITHUB` con tu usuario.

Pulsa **Watch → Custom → Issues + Pull requests + Releases** en su
repositorio para recibir solo lo relevante.

## Seguimiento semanal

- **Informe semanal** (lunes): el issue *Seguimiento semanal* te menciona y resume:
  - Commits de la semana y líneas cambiadas en la memoria.
  - Issues cerrados.
  - Barra de progreso de cada hito.
  - Alertas:
    - ⚠️ 14 o más días sin commits.
    - ⏰ Hitos vencidos con issues abiertos.
    - 🛑 Bloqueos.
    - 👀 PR con más de 7 días sin revisar.

  El alumno responde debajo con qué ha hecho, qué hará y qué le bloquea.
- **Tablero**: la vista *Roadmap* muestra el calendario, y la vista *Board* el trabajo en curso.
- **Dudas y bloqueos**: los issues con las etiquetas `duda` o `bloqueo` son los que esperan respuesta tuya.

## Revisar la memoria

- **Pull requests**: el alumno abre un PR por capítulo o bloque de cambios. La CI comenta con estadísticas (páginas, palabras, `\pendiente{}` abiertos, referencias sin definir) y adjunta:
  - el PDF completo;
  - un **PDF de cambios** (latexdiff: lo nuevo en azul, lo eliminado en rojo tachado). Así no tienes que releer lo que ya revisaste.
- Puedes comentar en tres sitios:
  - en líneas concretas del `.tex`, en la pestaña *Files changed*;
  - en el propio PDF (anótalo y súbelo al PR);
  - dentro del texto, con `\nota{...}` en un commit (sale en azul en el PDF).
- **Aprobar o pedir cambios** con *Review changes*. La etiqueta `cambios pedidos` ayuda a filtrar.

## Versiones

Las etiquetas publican una release con los PDF (memoria, presentaciones y cambios respecto a la etiqueta anterior):

| Etiqueta | Momento |
|---|---|
| `v0.3-seguimiento` | Presentación de seguimiento |
| `v0.9-borrador` | Borrador completo para revisión |
| `v1.0-entrega` | Versión depositada |
| `v1.1-defensa` | Versión final tras la defensa |

Las `v0.*` se marcan como *pre-release*. La release **Borrador** siempre contiene el último PDF de `main`.

## Consejos

- Pide objetivos medibles en la primera reunión (issue *Redactar objetivos*). Las conclusiones se contrastarán con ellos.
- Insiste en generar las figuras desde `scripts/figuras/`: evita capturas de pantalla y cifras copiadas a mano.
- El resumen de cada ejecución de la CI permite detectar de un vistazo una memoria con muchos `\pendiente{}` a pocas semanas de la entrega.
