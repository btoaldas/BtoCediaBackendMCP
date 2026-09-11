# Revisión del informe P3 versión 1

Fecha: 2026-09-10. Estado documental: **borrador**, únicamente por repositorio pendiente de publicación y acceso docente. No se publicó ni envió esta versión.

## Resultado

Entrada nueva: `privado/p03-informe-datos-v3.json`, derivada de v2, con `clase: "4"`. Salida nueva: `informes/practica-03/version-01/`, con PDF, DOCX editable y manifiesto de integridad. Ambos formatos tienen cinco páginas Letter. Se preservaron entradas, visores, capturas, fuentes y candidatos anteriores; el generador no se modificó.

Se incorporaron cuatro evidencias verificadas: `manual_registro` y `flujo_registro`, extractos renderizados desde los TXT conservados; `spec_manual` y `flujo_speckit`, PNG originales obtenidos mediante FireShot. Las capturas muestran el visor local de registros reales y se identifican como tales, sin presentarlas como terminal o TUI original. Sus bytes no se editaron.

Los dos registros de detalle se conservaron en `.tmp/qa-informes/p03-v1-registros/`, junto a su procedencia; el input v3 los referencia. Deben preservarse mientras esa entrada se utilice para regenerar. Su construcción determinista está en `.tmp/qa-informes/p03-v1-construir.py`: extrae campos de los bloques JSON de `registro-manual-v1.txt` y `registro-flujo-v1.txt`, ajusta líneas y dibuja el texto. No ejecuta de nuevo los casos ni simula salidas.

## Contenido contrastado

- Base P3: 55 pruebas, repartidas en 19 unitarias, 27 de integración y 9 e2e. No se incorporaron conteos de las ampliaciones de P4.
- Las 19 comprobaciones independientes de la versión manual se distinguen de las 19 unitarias de Spec Kit.
- Tres entradas idénticas en ambas versiones: `0 C F`, `-273.15 C K` y `NaN C F`, con sus resultados y códigos de salida. Se conserva la diferencia de mensajes de error y el límite de inferir equivalencia desde solo tres casos.
- Cobertura: 108/122 líneas, 88,52 %, mostrada por la herramienta como 89 %. Se declara que los subprocesos e2e no suman sus líneas a esa medición.
- Flujo de cuatro comandos reales, 33 tareas y defecto de empaquetado descubierto desde un entorno nuevo; la corrección termina con 55 aprobadas en 0,27 s.
- La comparación y conclusión se atribuyen como análisis técnico asistido, sin inventar percepciones personales. El efecto del pedido más preciso de Spec Kit está declarado.
- Los requisitos de capturas, versión manual y flujo/comparación están `cumplido` y enlazados a IDs de evidencia. Solo `repositorio` permanece `pendiente`.

## Revisión visual completa

Se renderizó el PDF con Poppler bundled y el DOCX mediante `render_docx.py` y LibreOffice headless bundled. No se utilizó la aplicación Word o LibreOffice desktop ni CUA durante esta producción.

Se inspeccionaron las cinco páginas finales de cada formato, diez páginas en total, a 120 dpi y sin omitir páginas. La primera composición dejaba el título de los tres casos separado de su tabla. La segunda incorporó la comparación explícita de casos borde ya documentada y mantuvo título, explicación y tabla juntos en la página 2, sin cambiar el generador.

| Página | Contenido revisado en PDF y DOCX | Resultado |
|---|---|---|
| 1 | Identificación, Clase 4, aviso de borrador, explicación y comparación | Texto y tabla completos; márgenes libres |
| 2 | Tres casos y registro manual de detalle | Título junto a la tabla; comandos, salidas y error legibles |
| 3 | Captura original del visor manual | Completa y sin retoque; el registro previo permite leer el detalle a escala Letter |
| 4 | Registro del flujo y conteos | Cuatro comandos y resultados legibles; base P3 explícita |
| 5 | Captura del flujo, verificación, conclusión y repositorio pendiente | Contenido completo y pies visibles |

No se observaron recortes, superposiciones, glifos defectuosos ni títulos huérfanos en la versión final. Las capturas conservan una vista global a escala menor; los registros separados proporcionan el detalle legible. Los espacios inferiores en páginas dedicadas a una figura se conservan para no dividir evidencias ni reducir su letra.

## Comprobación independiente

El validador devolvió `ok: true`, `estado: borrador`, cuatro evidencias. La revisión de OOXML encontró dos tablas y cuatro imágenes; los hashes de las cuatro imágenes incrustadas coinciden exactamente con sus PNG de origen. Se comprobaron hashes de entrada, fuentes, imágenes y ambos artefactos contra el manifiesto.

La extracción de ambos PDF confirmó cinco páginas de 612 × 792 pt y los literales críticos de clase, estado y conteos. Las diez páginas finales son idénticas píxel a píxel a su segunda composición revisada. Evidencia técnica: `.tmp/qa-informes/p03-v1-auditoria-final.json`; renderizados finales en `.tmp/qa-informes/p03-v1-pdf-final/` y `.tmp/qa-informes/p03-v1-docx-final/`.

Los renderizadores emitieron avisos de configuración/caché de Fontconfig; terminaron con código 0. No se modificó la caché ni la configuración y la inspección visual no mostró pérdida de texto.

| Artefacto | Bytes | SHA-256 |
|---|---:|---|
| `Informe-Practica-03.pdf` | 1138045 | `c4c8375eb608c7d27e67844f80623f7ac8aa5c5b657cd10945bf4e8964c7fb1d` |
| `Informe-Practica-03.docx` | 1357483 | `7429609a37245ccf62e310668eee27ab3dae98a8341700684a0a51eb8ccbebcf` |

Validación reproducible con Python documental:

```bash
python scripts/reportes_curso.py privado/p03-informe-datos-v3.json --validar
```

Una futura generación debe usar otra carpeta de salida. Para cerrar el borrador, aún se necesita una URL real de repositorio y comprobar el acceso del docente; después corresponde crear otra entrada/salida, actualizar las menciones al pendiente y repetir la revisión de esa versión. Esta revisión no acredita aceptación académica o recepción en AVAC.
