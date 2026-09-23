# Checklist de entrega

Confirma siempre la normativa vigente de tu escuela: esta lista es orientativa.

## Memoria (`v1.0-entrega`)

- [ ] `memoria/config/datos.tex` completo: título definitivo (igual que en la solicitud), fecha y titulación.
- [ ] Orden de las páginas: **portada → Anexo I firmado → portada** (`\AnexoItrue`).
- [ ] Resumen del proyecto y abstract con los 4 apartados y palabras clave.
- [ ] `make estadisticas` sin `\pendiente{}` ni `\nota{}`, y sin referencias sin definir.
- [ ] Sin avisos de «Overfull» visibles: revisa los márgenes en el PDF.
- [ ] Todas las figuras citadas en el texto, legibles impresas y vectoriales.
- [ ] Bibliografía completa, con formato homogéneo y DOI.
- [ ] Anexos: presupuesto con IVA y alineación con los ODS.
- [ ] Cumplimiento de objetivos contrastado en las conclusiones.
- [ ] Ortografía revisada (LTeX, y además una lectura en papel).
- [ ] Metadatos del PDF correctos (título y autor salen de `datos.tex`).

## Ficheros a subir

La release de la etiqueta `v1.0-entrega` contiene los PDF con los nombres ya preparados:

| Fichero | Origen |
|---|---|
| `TFG_Apellido1Apellido2_Nombre.pdf` | Memoria (release) |
| `Anexo_I_firmado_Apellido1Apellido2_Nombre.pdf` | `memoria/administrativo/AnexoI_firmado.pdf` |
| `Resumen_TFG_Apellido1Apellido2_Nombre.txt` | Resumen y abstract en texto plano (cabecera con título, titulación, autor, director y escuela) |
| Resumen breve (p. ej. 300 palabras) | Si la plataforma lo pide |

## Presentación de seguimiento (`v0.3-seguimiento`)

- [ ] `presentacion/seguimiento.pdf`: objetivos, trabajo hecho, resultados preliminares, planificación y riesgos.

## Defensa (`v1.1-defensa`)

- [ ] `presentacion/defensa.pdf`: aproximadamente una diapositiva por minuto.
- [ ] Ensayo cronometrado con el director.
- [ ] Lista de preguntas previsibles del tribunal y sus respuestas.
- [ ] Copia del PDF en un USB y en la nube.

## Reproducibilidad

- [ ] README del código: instalación, datos (DOI), semillas y comandos exactos.
- [ ] `make figuras` regenera todas las figuras.
- [ ] La etiqueta `v1.0-entrega` corresponde exactamente a la versión depositada.
