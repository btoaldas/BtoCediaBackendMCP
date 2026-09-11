# Nota metodológica de la comparación

La práctica es de recuperación, realizada fuera de las sesiones originales.
No se atribuyen los tiempos de la guía (30 minutos por bloque) como tiempos
medidos, ni se afirma asistencia a clase. Las fechas de archivos y registros
corresponden a esta ejecución.

En 3.A la spec manual se redactó antes del código. agy recibió esa spec completa
por `--print`, devolvió código textual real y Codex lo guardó sin cambios y lo
probó. Las herramientas del primer intento headless fueron denegadas; el código
no procede de una llamada simulada ni de un mock. El borrador Codex
anterior se conserva en el histórico local y en Git previo; la presentación
actual incluye únicamente conversor_agy.py como implementación evaluada.

En 3.B Specify CLI se instaló temporalmente con uvx desde el repositorio oficial
GitHub Spec Kit, commit c173bf19a6654e3b05386ec3599349a55282b897. `specify init`
usó la integración agy y creó los skills reales. Se invocó /speckit-specify desde
la TUI de agy, con permisos concedidos por acción y raíz acotada a esta práctica.
Los artefactos de cada fase se conservan para demostrar la secuencia.

Ambos bloques resuelven el mismo conversor. El pedido de Spec Kit solicitó
además explicitar NaN/Infinity y límites de magnitud/longitud. Por ello, la
ampliación no se atribuye exclusivamente al framework: también existe una
diferencia deliberada en la precisión del pedido. La comparación principal
usa exactamente los mismos tres casos en ambas implementaciones.

Las reflexiones redactadas por Codex describen conclusiones técnicas derivadas
de evidencia. No se presentan como sensaciones o experiencias personales de
la persona matriculada. La calificación y aceptación corresponden al docente.

En P4, el primer tester-agent nativo ejecutó 55 pruebas y produjo un mapa de
trazabilidad. Una revisión independiente reprodujo después un incumplimiento
de FR-012 con `1e9999999`: cobertura y todos los tests en verde no demostraban
que cada posible entrada estuviera bien tratada. Se solicitó al mismo tester
una regresión y al principal una corrección; se conserva el primer informe.
