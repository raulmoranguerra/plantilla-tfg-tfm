# Guía del director

## Preparar la plantilla (una vez)

1. Sube este repositorio a GitHub (a tu cuenta o a una organización del grupo).
2. **Settings → General → Template repository ✅**. Así los alumnos verán el botón *Use this template*.
3. Adapta a tu grupo, si quieres:
   - `.github/proyecto/plan.yml`:
     - `director:`, con tu usuario de GitHub. El informe semanal te mencionará.
     - Los hitos (con su posición relativa en el calendario), las etiquetas y las tareas iniciales. Por ejemplo, añade la tarea «Entregar el informe de seguimiento a la plataforma» o elimina el Anexo I si no aplica.
   - `memoria/config/datos.tex`: titulación, escuela y logo por defecto.
   - `memoria/capitulos/`: la estructura de capítulos que prefieras.
4. Comprueba que el workflow **Compilar** está en verde en la plantilla.
5. En tu ordenador, clona la plantilla y prepara las herramientas del director:
   ```bash
   gh auth refresh -s project        # permiso para crear tableros (una vez)
   pip install pyyaml
   ```
6. (Opcional, recomendado) Crea en tu cuenta un tablero de Projects llamado
   **«Plantilla tablero TFG»** y configúralo a tu gusto:
   - una vista *Board* agrupada por *Status*;
   - una vista *Roadmap* por *Milestone*;
   - los campos que quieras.

   Los tableros de los alumnos se crearán como copia suya, ya configurados.

> En la propia plantilla, los workflows de inicialización e informe
> semanal detectan que es una plantilla y no hacen nada.

## Alta de un alumno

El alumno solo sigue los pasos 1 a 3 de la [guía del alumno](GUIA_ALUMNO.md):

1. Crea su repositorio desde la plantilla.
2. Te invita como colaborador. Acepta la invitación que te llega por correo.
3. Rellena sus datos.

Después, desde la carpeta de la plantilla en tu ordenador, ejecuta:

```bash
make alta REPO=alumno/tfg-repo INICIO=2026-10-01 SEMANAS=36
```

Este comando:

- Crea en su repositorio las etiquetas, los 8 hitos con fecha y los 24 issues iniciales.
- Crea en **tu** cuenta el tablero `tfg-repo · seguimiento` con todos esos issues.
- Comparte el tablero con el alumno como editor.

Se puede volver a ejecutar sin duplicar nada, por ejemplo para mover las
fechas de los hitos.

> **¿Por qué no se crea el tablero automáticamente?** Los tableros de GitHub
> Projects pertenecen a un usuario, no a un repositorio. El token de GitHub
> Actions solo tiene permisos sobre el repositorio, así que no puede
> crearlos. Por eso los creas tú con tu `gh`, y el alumno no tiene que
> configurar ningún token.

Pulsa **Watch → Custom → Issues + Pull requests + Releases** en su
repositorio para recibir solo lo relevante.

## Seguimiento

### Panel de todos tus alumnos

```bash
make seguimiento
```

```
Alumno                   Últ. commit  Hito actual                     Prog.  Bloq. Dudas  PR  Versión
ana/tfg-baterias            hace 2 d  H1 · Estado del arte (10/12)      50%      0     1   1  v0.1-arranque
luis/tfg-vision            hace 16 d  H1 · Estado del arte (10/12)      25%      1     0   0  —
                                      ⚠️  16 días sin commits
                                      🛑 1 bloqueo(s)
```

Además, añade a cada tablero los issues nuevos que hayan abierto los
alumnos. Como el tablero está en tu cuenta y el repositorio en la suya,
GitHub no los añade solo. Ejecútalo antes de cada reunión, o cada lunes.

### Informe semanal (automático)

Cada lunes se abre en el repositorio de cada alumno un issue *Seguimiento
semanal* que te menciona, con:

- Commits de la semana y líneas cambiadas en la memoria.
- Issues cerrados.
- Barra de progreso de cada hito.
- Alertas:
  - ⚠️ 14 o más días sin commits.
  - ⏰ Hitos vencidos con issues abiertos.
  - 🛑 Bloqueos.
  - 👀 PR con más de 7 días sin revisar.

El alumno responde debajo con qué ha hecho, qué hará y qué le bloquea.

### Tablero y dudas

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
