# QA de la entrega de práctica 2

Resultado: **APTO para la entrega documental**, sin defectos materiales de contenido o maquetación observados. Esta revisión verifica los archivos locales; no acredita envío, recepción ni calificación en el AVAC.

Se revisó `informes/practica-02/version-02-final/`, generado desde `privado/p02-informe-datos-v3-final.json`. La revisión fue independiente de la generación y no modificó el input, el generador ni los entregables.

## Método y evidencia

- PDF: render de sus **7 páginas** con Poppler `pdftoppm -r 150 -png` del runtime incluido de Codex.
- DOCX: render de sus **7 páginas** con `render_docx.py --emit_pdf --verbose` y LibreOffice del mismo runtime, sin utilizar la instalación de escritorio.
- Inspección visual de **14 páginas** mediante `view_image`; el DOCX se revisó también a resolución original para evitar dudas introducidas por la reducción del visor.
- Contraste de texto en PDF final, OOXML del DOCX y PDF renderizado por LibreOffice.
- Comprobación de hashes del input, los dos entregables, las siete imágenes y sus siete fuentes. También se compararon los bytes de las siete imágenes incrustadas en el DOCX con sus originales.

Los renders, extracciones y resultados verificables permanecen en `.tmp/qa-informes/p02-final-*`. Los resúmenes estructurados son `p02-final-audit.json` y `p02-final-content-checks.json`.

## Revisión visual por página

| Página | Contenido común a PDF y DOCX | Resultado |
| --- | --- | --- |
| 1 | Identificación, explicación, método asistido y tabla de tiempos | Texto completo, tabla dentro de página y título de comparación acompañado por su explicación. |
| 2 | Tabla de predicciones y primer registro | Filas completas, anchos útiles y registro legible con descripción unida. |
| 3 | Registros de email y usuarios | Ambos registros completos, datos y pies legibles, sin colisión con el pie de página. |
| 4 | Registro del cierre | Contraejemplo, causa, AssertionError y exit 1 visibles; descripción completa. |
| 5 | Capturas reales del visor de rondas 1 y 2 | Ambas capturas y descripciones completas. El inicio de ronda 3 que se ve dentro de la segunda captura pertenece a la imagen fuente del visor. |
| 6 | Captura del cierre, reproducción y alcance de comparación | Captura y descripción presentes; comandos y limitaciones completos, sin desbordamientos. |
| 7 | Comparación docente y tres reflexiones | Tabla íntegra y tres respuestas completas en la misma página, sin títulos huérfanos. |

Las capturas del visor tienen texto pequeño por su ancho de origen; los cuatro registros ampliados de páginas 2–4 permiten leer los mismos resultados con mayor comodidad. Se conserva esta combinación para mostrar procedencia y contenido. No se observaron recortes, solapamientos, caracteres ausentes ni separación problemática entre figuras y pies.

La sospecha inicial de ausencia del pie de captura 7 en el DOCX se descartó al abrir la página 6 a resolución original y contrastar el texto del PDF de LibreOffice. No requirió cambio.

## Contenido comprobado

- Tres reflexiones asistidas, presentes exactamente una vez cada una y completas respecto al input final, en los tres canales de extracción.
- Siete encabezados de evidencia y siete descripciones presentes: cuatro registros renderizados y tres capturas reales del visor. Las siete imágenes incrustadas en DOCX son idénticas por SHA-256 a los archivos fuente.
- Recuperación asincrónica y predicciones atribuidas al asistente; no se atribuyen experiencias presenciales ni vivencias anteriores al estudiante.
- Comparación posterior con fuente y marcas temporales. Se conserva expresamente que **no se confirmó resultado ni falla del cierre del instructor** y que los factores de modelo, contexto y canal no se controlaron.
- Falla propia conservada y explicación de que el laboratorio no tiene autenticación ni API desplegada.
- Ninguna sección de repositorio exigida para P2; no hay rutas absolutas privadas en el texto extraído.
- Los hashes de todos los artefactos y fuentes coinciden con el manifiesto; los entregables conservan los mismos hashes al finalizar la revisión.

## Integridad de la versión revisada

| Archivo | Bytes | SHA-256 |
| --- | ---: | --- |
| `Informe-Practica-02.pdf` | 2698998 | `7ee4001e3e322ce0d2e7708ac55c3abea9a9d9b2383c29f919cd3dba774b6b04` |
| `Informe-Practica-02.docx` | 2626961 | `17966f02b53f00ea2c869a11d61079c873f8a01c2406e307423268dd462ef667` |

SHA-256 del input final: `c1cd7516a863667f8da89c8f9daad4314094ec4e3ad1a6d352a5bd330e563469`.

No se ejecutaron nuevas rondas, cambios al código experimental ni acciones en CEDIA durante este QA. La falla intencional permanece conservada.
