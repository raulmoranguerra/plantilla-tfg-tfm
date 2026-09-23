# Guía de estilo LaTeX

## Referencias cruzadas

- Etiqueta todo lo que vayas a citar, con un prefijo:

  | Prefijo | Para |
  |---|---|
  | `cap:` | capítulos |
  | `sec:` | secciones |
  | `fig:` | figuras |
  | `tab:` | tablas |
  | `ec:` | ecuaciones |
  | `lst:` | código |
  | `alg:` | algoritmos |
  | `anx:` | anexos |

- Referencia con `\cref{...}`, que escribe «figura 3.2», «tabla 4.1», «anexo A». Al inicio de frase usa `\Cref{...}`.
- Toda figura y tabla debe citarse en el texto antes de aparecer.

## Números y unidades

- Usa siunitx siempre: `\num{3.91}` → 3,91; `\qty{25}{\milli\second}` → 25 ms; `\qty{21}{\percent}`.
  En el `.tex` se escribe **punto** decimal; siunitx imprime la **coma**. En el abstract en inglés se imprime el punto automáticamente.
- Fuera de siunitx, en modo matemático escribe `3{,}91`; si no, la coma deja un espacio de más.
- Magnitudes en cursiva (`$V$`), unidades en redonda (siunitx ya lo hace).

## Figuras

- **Vectoriales** (PDF) siempre que se pueda. Usa PNG o JPG solo para fotos.
- Las gráficas con datos se generan con `scripts/figuras/` (plantilla: `ejemplo_curva.py`). Se guardan en `figuras/generadas/`, con la tipografía de la memoria y coma decimal. Nunca uses capturas de pantalla de gráficas.
- Los diagramas de bloques pueden hacerse en TikZ (ver capítulo 3) o en draw.io exportando a PDF.
- `\includegraphics` sin extensión y sin `figuras/` delante: `\includegraphics{generadas/mi_figura}`.
- El pie de figura se entiende sin leer el texto.

## Tablas

- Usa booktabs (`\toprule`, `\midrule`, `\bottomrule`), sin líneas verticales.
- Alinea números por la coma decimal con la columna `S` de siunitx (ejemplo en el anexo de presupuesto).
- Las tablas de resultados se generan desde Python con `guardar_tabla()` para evitar errores al copiar cifras.
- El título va **encima** de la tabla.

## Bibliografía

- Usa un gestor (Zotero con Better BibTeX) y exporta a `bibliografia/referencias.bib`.
- Claves `AutorAñoTema` (por ejemplo `Chemali2018LSTM`), con DOI siempre que exista.
- Cita el trabajo original, no el blog que lo resume.

## Acrónimos

- Defínelos en `preliminares/acronimos.tex` y úsalos con `\ac{...}`: se expanden la primera vez y aparecen solos en la lista. En títulos y pies de figura escribe la sigla como texto normal (sin `\ac`), porque si no su «primera aparición» ocurre en el índice.

## Notas de trabajo

- `\pendiente{texto}` marca en rojo lo que falta por hacer. La CI los cuenta en cada compilación.
- `\nota{texto}` añade comentarios en azul (del director o tuyos).
- Antes de la entrega no debe quedar ninguno (`make estadisticas`).

## Redacción

- Usa la impersonal o la primera persona del plural, de forma coherente en toda la memoria.
- Escribe frases cortas, **una por línea en el `.tex`**.
- No uses anglicismos si existe término en español. Si no existe, escríbelo en cursiva: *machine learning*.
- La extensión LTeX de VS Code revisa ortografía y gramática en español mientras escribes.
