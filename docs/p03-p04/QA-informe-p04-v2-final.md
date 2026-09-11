# QA del informe P4 — versión 02 final

Fecha: 10 de septiembre de 2026, Ecuador. Resultado: **APTO DOCUMENTAL PARA ENTREGA**.

El input `privado/p04-informe-datos-v7-final.json` valida en estado `final`: seis requisitos cumplidos, ninguno pendiente y tres evidencias verificadas. Conserva las capturas reales B/E sin alterarlas y distingue el registro renderizado de publicación de una captura de interfaz. El commit inmutable citado es `65a1b1225f9a8fb105308e8c076fc8b52b89eda3`.

## Artefactos revisados

| Archivo | Páginas | Bytes | SHA-256 |
|---|---:|---:|---|
| `informes/practica-04/version-02-final/Informe-Practica-04.pdf` | 5 | 944324 | `3a0b934a4ea877898233a3e78d9bc6eb872e793c78e3b40077bf5925e5c355f6` |
| `informes/practica-04/version-02-final/Informe-Practica-04.docx` | 5 | 1140458 | `3d044acc383b6d3c881b4a26151ebfcb294a2c5e1aadf60ca16b774e0ea04688` |

Input SHA-256: `7b8343ea317216ad55df2ec89e8e1604095e36db4f30371a4a0f2acfd511f53c`.

## Verificación visual y estructural

Se renderizó el PDF mediante Poppler y el DOCX mediante el LibreOffice headless del runtime bundled; se inspeccionaron individualmente las diez páginas resultantes. Todas son Letter, 612 × 792 pt. Texto, tablas, imágenes y pies son legibles y no presentan recortes ni encabezados huérfanos. La tabla de resultados comienza en la página 2 junto a su encabezado. La figura E ocupa la página 3 con su pie completo; el espacio inferior es consecuencia de conservar íntegra la siguiente figura. El registro de publicación queda legible en la página 4.

El primer candidato, preservado en temporales, separaba el encabezado de resultados de su tabla. El segundo incorporó la explicación verificable de las condiciones del veredicto y controles de higiene; resolvió el salto sin cambiar el generador. Las cinco páginas PDF finales coinciden píxel a píxel con ese candidato revisado.

El DOCX contiene dos tablas editables y tres PNG incrustados byte a byte iguales a las fuentes. El PDF conserva el texto crítico de resultados, URL y commit. No contiene marca de borrador, requisitos pendientes ni rutas personales absolutas. El manifiesto coincide con tamaños, hashes e input. Las rutas de fuentes y metadatos del input resuelven desde `privado/`, y todos sus hashes se verificaron, incluido el replay canónico. El PNG del registro de publicación se conserva en `.tmp/qa-informes/p04-v2-candidato/publicacion-p04-registro.png`; ese temporal es dependencia del input reproducible y no debe retirarse.

## Procedencia y límites

El bloqueo B corresponde al segundo cierre de la ejecución real: 9 fallos, 51 aprobados, exit 1, decisión continue; tras la corrección se conservan 60 aprobados. E documenta el segundo fallo preparado (5 fallos, 60 aprobados), su corrección y el reporte de 65/65, 94,3 %. La base histórica P3 de 55 pruebas permanece diferenciada.

La captura del reporte E conserva su fecha del 10/09/2026 a las 21:34:42 Ecuador. La segunda reproducción canónica, a las 21:51:32, está identificada aparte y no se atribuye a la captura anterior. Las conclusiones técnicas no se presentan como sensaciones ni reflexión oral del estudiante. La revisión de seguridad y el patrón automatizado no se presentan como certificación de seguridad.

El registro de publicación pública anónima contiene cinco lecturas HTTP 200. Esta revisión contrastó nuevamente sus cinco archivos mediante `git show` contra el commit inmutable: tamaños y SHA-256 idénticos. No repitió navegación ni modificó el repositorio. El acceso público acredita disponibilidad para el docente, no una visita, revisión ni aceptación académica.

Los artefactos de `version-01-borrador/` mantienen sus hashes originales. No se editaron el generador, las fuentes B/E ni inputs anteriores. El artefacto final está preparado para carga en AVAC; esta QA no acredita su envío o recepción.

Auditoría estructurada: `.tmp/qa-informes/p04-v2-auditoria-final.json`. Renders: `.tmp/qa-informes/p04-v2-pdf-final/` y `.tmp/qa-informes/p04-v2-docx-final/`.
