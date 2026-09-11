# Comparación P3 — especificación manual y Spec Kit

Comparación de dos implementaciones del mismo conversor de temperatura. Las
observaciones son técnicas, basadas en archivos y ejecuciones reales; no se
atribuyen sensaciones personales al estudiante ni tiempos que no se midieron.

| Aspecto de la guía | Spec a mano | Spec Kit |
|---|---|---|
| ¿Cubrió los mismos casos borde? | Definió entrada ausente/no numérica, unidad igual, cero absoluto exacto y negativos válidos. La implementación además rechazó NaN por iniciativa de agy. | Conservó esos casos y explicitó NaN/Infinity, longitud bruta de 32 caracteres, magnitud máxima de 1e12, notación científica, redondeo half-up y cero con signo. |
| ¿Qué generó Spec Kit que no estaba escrito? | Un objetivo, cinco criterios verificables y cuatro casos borde en una spec breve. | Tres historias, 18 escenarios de aceptación, 13 requisitos funcionales, modelo de datos, contrato CLI, plan, investigación, quickstart, checklist y 33 tareas. |
| ¿Qué se sintió más rápido de arrancar? | No se registró una percepción personal. Objetivamente requirió una spec y una llamada de generación de código. | No se registró una percepción personal. Requirió inicialización oficial y cuatro fases explícitas antes de cerrar implementación. |
| ¿Cuál generó más confianza en el resultado? | Evidencia acotada: tres casos comparativos y 19 comprobaciones independientes de criterios. | Evidencia más amplia: tres capas de pruebas, estados rojos conservados, cobertura y segunda revisión desde un entorno nuevo; esta última detectó un fallo de empaquetado que las primeras pruebas no mostraban. |

La petición a Spec Kit incluyó expresamente límites y valores no finitos. Por
eso, la ampliación de detalle no se atribuye exclusivamente a la herramienta:
también influyó una petición más precisa. La constitución inicial era una
plantilla sin ratificar, no una aprobación; `tasks.md` documenta esa distinción.

## Los mismos tres casos

Corrida real: `evidencia/p03-p04/comparacion-corridas/20260911T012725.506823Z/casos.json`.

| Tipo | Entrada | Spec manual (`conversor_agy.py`) | Spec Kit (`python -m temperatura`) |
|---|---|---|---|
| Normal | `0 C F` | `32.00 F`, exit 0, stderr vacío | `32.00 F`, exit 0, stderr vacío |
| Borde definido | `-273.15 C K` | `0.00 K`, exit 0, stderr vacío | `0.00 K`, exit 0, stderr vacío |
| No contemplado en la spec manual | `NaN C F` | stdout vacío, error argparse en stderr, exit 2 | stdout vacío, error de literal no permitido en stderr, exit 2 |

Los tres resultados coinciden en comportamiento observable. Tres casos no
prueban equivalencia completa entre las dos implementaciones.

## Cierre técnico propuesto

Para un proyecto pequeño y acotado, una spec manual con criterios comprobables
puede bastar; para uno mediano con varios requisitos y trazabilidad, Spec Kit
aporta una secuencia de especificación, diseño, tareas y pruebas revisables.
Esta es una recomendación técnica derivada de la práctica, no una preferencia
personal atribuida al estudiante.
