# Resultados 3.A

La spec completa se pegó en una llamada real `agy --print`. La herramienta devolvió
el código que se conserva sin modificaciones en `conversor_agy.py`. Codex guardó
el bloque Python y ejecutó los tres procesos porque el modo headless de agy
denegaba las herramientas. La limitación y la intervención están declaradas;
no se atribuye la ejecución de los tests a agy.

| Caso | Entrada | stdout | Exit | Resultado |
|---|---|---|---|---|
| normal | 0 C F | 32.00 F | 0 | Conversión correcta |
| borde spec | -273.15 C K | 0.00 K | 0 | Conversión correcta |
| no contemplado | NaN C F | (vacío) | 2 | Rechazo controlado en stderr |

NaN no estaba contemplado en la spec manual. agy agregó validación de finitud por iniciativa; ese comportamiento se observó en la ejecución real.

Evidencia pública: [resultados y procedencia](../../evidencia/p03-p04/publicable/p03-resultados-base-v2.json) y [captura del visor manual](../../evidencia/p03-p04/capturas-p03/manual-v1.html). La respuesta agy y los procesos originales se conservan localmente según sus hashes. El borrador Codex previo permanece en el histórico local y Git anterior; no forma parte de la implementación evaluada.
