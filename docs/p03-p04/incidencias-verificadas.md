# Incidencias verificadas durante P3

## P3.A — herramientas headless

La primera llamada real de agy recibió denegación de sus herramientas. Se
preservó el registro. La solución autorizada fue enviar la spec completa en el
prompt de `agy --print`, conservar su respuesta y guardar el bloque Python sin
cambios. Codex ejecutó los procesos. La diferencia se declara en resultados-3a.

## P3.B — empaquetado descubierto por e2e y segunda revisión

En la primera ejecución después de implementar US1, 12 pruebas pasaron y dos
e2e fallaron con `No module named temperatura`. El registro original está en
`tdd-logs/us1_primer_intento_empaquetado_fallido.log`. `uv pip install -e .`
permitió continuar en ese entorno y la suite funcional llegó a 55 aprobadas.

La verificación independiente `verificar_entorno_fresco.py` creó un entorno
nuevo, conservando el anterior. El 11 de septiembre a 01:23:11 UTC observó:
`uv sync --frozen` exit 0; CLI exit 1 y ocho e2e fallidas, 46 pruebas aprobadas.
Ese conteo fue anterior a incorporar el test de rendimiento. El fallo confirmó
que el editable instalado manualmente ocultaba una declaración de empaquetado
incompleta: no existía `[build-system]` y uv consideraba virtual el proyecto.

Se entregó ese diagnóstico al mismo agy para corregir `pyproject.toml`, generar
README y actualizar lock/sync. Los registros previos se preservan; el cierre
requiere otra corrida completa en un entorno nuevo.

## P3.B — coherencia de la longitud

La spec limitó a 32 caracteres el valor recibido. T026 inicialmente usó
`len(raw_input.strip())`, permitiendo que espacios exteriores eludieran el
límite. Se señaló la contradicción antes de implementar US3. agy corrigió
T026 a `len(raw_input)` y creó una prueba con relleno de espacios. La fase roja
US3 tuvo 14 fallos; su fase verde tuvo 22 aprobadas.

## Interpretación del TDD

US1 comenzó con error de importación durante colección (exit 2), porque aún
faltaban objetos de dominio. No se presenta como una aserción funcional fallida.
US2 sí observó siete aserciones fallidas antes de añadir el límite físico;
US3 observó 14 fallos antes de incorporar controles de entrada. Se conservan
fuentes de esos estados y los logs reales.

La corrección quedó comprobada independientemente en
`entorno-fresco/20260911T013135.411265Z/resultados.json`: sincronización exit 0,
CLI `32.00 F` exit 0 y **55 aprobadas en 0,27 s** desde otro entorno nuevo.
El paquete declara `setuptools.build_meta` con descubrimiento en `src`.

## P4.A — FR-012: exponente extremo

La revisión independiente del código planteó un valor finito de cadena corta:
`1e9999999`. El proceso real terminó con exit 1 y traceback `decimal.Overflow`
en `abs(valor)`, antes de comparar con `1e12`. `abs` aplica el contexto Decimal;
`copy_abs()` permite comparar la magnitud sin ese desbordamiento. Se entregó
el hallazgo al tester-agent y al agente principal para regresión y corrección.
El estado original está conservado en `09-qa-fr012-overflow-detectado`.

La misma revisión ejecutó `sNaN` y `NaN12`: ambos se rechazaron correctamente con
exit 2. Esto refuta la interpretación inicial del informe de tester de que la
comprobación `is_finite()` era redundante. El informe original se conserva y
la corrección debe distinguir cobertura observada de cobertura supuesta.

La regresión del tester produjo **3 fallos y 2 aprobadas** (55 deseleccionadas):
falló dominio, integración y proceso e2e para el exponente extremo. Tras la
corrección a `copy_abs()` en CLI y dominio, once comprobaciones independientes
pasaron el 11 de septiembre a 01:47:53 UTC, incluida una magnitud apenas superior
a `1e12` que no debe redondearse antes de compararla. Registro:
`verificacion-final/20260911T014753.368247Z/resultados.json`.

## P4 — precisión intermedia y doble redondeo

Otra revisión independiente detectó que el valor válido
`1.0027777777777777777777777777 C F` producía `33.81 F`. El oráculo de aritmética
racional exacta (Fraction) da `33.80499999999999999999999999986`, cuyo redondeo
half-up correcto es `33.80 F`. La entrada vecina terminada en `...7778` produce
`33.80500000000000000000000000004` y debe redondear a `33.81 F`. Ambos procesos
se ejecutaron y quedaron registrados en
`qa-redondeo/20260911T015453.446522Z/resultados.json`.

La precisión global Decimal de 28 dígitos redondeaba un intermedio antes de
formatear. Se solicita regresión a ambos lados y contexto local de precisión
suficiente para el contrato de 32 caracteres. La copia B ya creada se conserva
con su base de 60 pruebas: su propósito es demostrar el ciclo del hook; el
arreglo numérico se aplica a la base canónica y será la base de E.


## Cierre de precisión y evidencia Stop

La corrección nativa de agy usa `localcontext()` con precisión 80 al convertir y
formatear, sin cambiar el contexto global. La suite ampliada alcanza 65 pruebas
(23 unitarias, 31 de integración, 11 e2e). Una instalación con `uv sync --frozen`
en un entorno virtual nuevo volvió a aprobar las 65, y dos procesos CLI
independientes devolvieron `33.80 F` y `33.81 F` a ambos lados del umbral racional.
La evidencia derivada está en `evidencia/p03-p04/publicable/p04-redondeo-corregido.json`.

En el escenario B, previo a esa ampliación de precisión, agy alteró la constante
C→F de 32 a 32.05. El segundo turno produjo un Stop auténtico con 9 fallos y 51
aprobados (exit 1, decision=continue). Tras restaurar 32, otro Stop aprobó las 60
pruebas y respondió `{}`. No se determinó por qué el primer turno tras trust no
ejecutó el hook; no se atribuye una causa sin demostración. Se verificó que el
runtime ejecuta el comando relativo al directorio que contiene `hooks.json`.

En E, Codex preparó un fallo distinto y explícito, sustituyendo ROUND_HALF_UP por
ROUND_DOWN en el método de formato de una copia aislada. El Stop real de la
orquestación produjo 5 fallos y 60 aprobados; agy restauró el redondeo correcto.
La primera carga de subagentes no disponía de ejecución y se registró como
limitación del runtime, sin atribuir al tester comandos del principal. Se
reanudó usando la definición dinámica nativa con capacidad de escritura y los
permisos por acción del CLI; ninguna configuración global se amplió.
