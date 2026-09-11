# Práctica 2 — notas del experimento guiado

## Estado final y lectura de estas notas

La práctica 2 fue enviada para calificar a las 20:45 del 10/09/2026; la descarga AVAC coincide con el PDF final. Se aportaron tres capturas reales del visor, siete evidencias y tres reflexiones asistidas. La [comparación vigente con el instructor](../docs/p02/instructor-comparacion-v2.md) verifica las rondas 1–3; el resultado del cierre del instructor no fue confirmado. Véase la [QA final](../docs/p02/QA-entrega-v1.md).

El registro que sigue se conserva literalmente: las frases «no disponible» y los pendientes de composición describen el momento previo a la consulta posterior y a la entrega. No son el estado actual. Se mantienen las predicciones prospectivas y la atribución de las reflexiones al asistente.

## Registro histórico de ejecución

Recuperación asincrónica ejecutada el 10 de septiembre de 2026 (America/Guayaquil), con Python 3.12.13, uv 0.11.14 y agy real, Gemini 3.8 Flash (High). Las predicciones y reflexiones técnicas pertenecen al agente asistente Codex; no se presentan como vivencias o respuestas personales de Alberto.

Este documento consolida las notas después de la ejecución. Las predicciones originales fueron guardadas prospectivamente en `evidencia/p02/prediccion-01.json` a `prediccion-04.json`; la verificación de tiempos, pedidos y hashes está en `evidencia/p02/trazabilidad.txt`. No se dispone de resultados del instructor.

## Canal de ejecución y fidelidad

Se mantuvieron los cuatro pedidos literales como primera línea. El modo headless inicial denegó una lectura y otro intento agotó dos minutos sin salida; ninguno cuenta como ronda ejecutada. Las cuatro respuestas útiles se obtuvieron con `agy --print`, añadiendo una nota operativa de no usar herramientas y devolver código Python. En rondas 2 a 4 se incluyó, sin alterar, el código anterior. Codex guardó y ejecutó la respuesta. La envoltura completa está conservada en `prompt-XX-ejecutado.txt`.

Esta adaptación conserva la evolución sobre el código anterior, pero no equivale a la interacción sincrónica de aula ni acredita aceptación del docente. Los snapshots son copias exactas del bloque Python de cada respuesta; no se corrigieron ni embellecieron después.

## Ronda 1 — contraseñas

Pedido: `hazme un validador de contraseñas`

Predicción original: 2026-09-11 00:32:59.973032 UTC. Respuesta útil: 00:45:35.235860 a 00:46:21.264050 UTC. Prueba Python: 00:48:03.476228 UTC.

| Pregunta | Predicción del asistente | Resultado real | Instructor |
|---|---|---|---|
| Longitud mínima | 8 caracteres | 8; añadió además máximo 128 | No disponible |
| Composición | Mayúscula, minúscula, número y símbolo | Exigió las cuatro clases | No disponible |
| Contraseña vacía | Rechazada con requisitos incumplidos | Rechazada; cinco errores, fuerza Débil | No disponible |

`12345`, `password` y vacío fueron rechazados. La prueba adicional `Ab3!xy7Z` fue aceptada, mientras `Ab3!xy7` fue rechazada por longitud. El generador añadió una lista de subcadenas prohibidas y veto a espacios sin que el pedido lo indicara. También llamó «listo para producción» a su respuesta; ese calificativo es una afirmación del generador y no una conclusión de estas pruebas.

Evidencia: `resultado-01.txt`, `cli-01.txt` y snapshot `s3/rondas/01-contrasenas/main.py`.

## Ronda 2 — email

Pedido: `agrégale que también valide un formato de email`

Predicción original: 2026-09-11 00:48:52.637872 UTC, anterior al inicio 00:48:52.700972 UTC. Resultado Python: 00:50:35.715053 UTC.

| Pregunta | Predicción del asistente | Resultado real |
|---|---|---|
| Formato de respuesta | Conservar is_valid/errors; strength vacío u omitido para email | Misma dataclass; strength pasó a opcional y vale null para email |
| Email `ana@` | Rechazado por dominio incompleto | Rechazado: dominio vacío |
| Email vacío | Rechazado por formato | Rechazado con mensaje específico de vacío |

`ana@correo.com` fue aceptado. Se compararon seis contraseñas contra la ronda 1: todas conservaron exactamente is_valid, errors y strength. Se ejecutó también el bloque CLI original. La afirmación del generador sobre conformidad RFC no se certifica con estos casos acotados.

Evidencia: `resultado-02.txt`, `cli-02.txt` y snapshot `s3/rondas/02-email/main.py`.

## Ronda 3 — lista de usuarios

Pedido: `ahora que maneje una lista de varios usuarios, cada uno con su contraseña y su email`

Predicción original: 2026-09-11 00:50:35.774545 UTC, anterior al inicio 00:50:35.808947 UTC. Resultado Python: 00:52:26.848119 UTC.

| Pregunta | Predicción del asistente | Resultado real |
|---|---|---|
| ¿Se rompería algo previo? | Las funciones anteriores probablemente se conservarían | Nueve respuestas de campo conservaron sus resultados |
| Estructura de usuarios | Lista de objetos dataclass User en memoria | Lista de User con username, email y password; resultados UserValidationResult |

Se agregaron dos usuarios sintéticos a una lista vacía y se imprimió la lista completa. Ambos resultaron válidos. El agente añadió dos reglas no solicitadas: username no vacío y correos duplicados que invalidan ambos usuarios del lote. Los datos viven en memoria; no se creó una base de datos.

Evidencia: `resultado-03.txt`, `cli-03.txt` y snapshot `s3/rondas/03-usuarios/main.py`.

## Cierre — cambio para administradores

Pedido: `ahora que la validación de contraseña sea opcional para usuarios administradores`

Predicción original: 2026-09-11 00:52:26.904771 UTC, anterior al inicio 00:52:26.937241 UTC. Resultado Python: 00:54:52.917583 UTC.

Se predijo el riesgo de saltar también el email y se esperó una opción para forzar la validación del administrador. El email siguió validándose: el administrador con `ana@` fue rechazado. Sí apareció la opción `validate_admin_password`.

| Entrada con contraseña `12345` | Resultado real |
|---|---|
| is_admin=False, booleano | Usuario inválido |
| is_admin="false", texto | Usuario válido, contraseña «Débil (Opcional - Admin)» |
| is_admin="usuario", texto | Usuario válido, misma exención |
| is_admin=True y validación forzada | Usuario inválido |

La falla se provocó introduciendo el nuevo indicador como texto. `User` es una dataclass con anotación bool, pero no comprueba el tipo en ejecución; `if user.is_admin` trata cualquier cadena no vacía como verdadera. La reproducción desde JSON creó el objeto con `User(**json.loads(payload))`, lo procesó por `validate_users` y produjo un AssertionError al exigir que se rechazara. Exit code real: 1.

Esto demuestra una inconsistencia alcanzable en la API Python del laboratorio. No demuestra una escalada de privilegios en un sistema desplegado: aquí no hay autenticación, servicio HTTP ni usuarios reales. La falla se conserva como evidencia del experimento; no es código aprobado para producción.

Frase de reporte técnico: **«El texto 'false' activa la excepción de administrador, por lo que una contraseña rechazada por la función directa pasa al validar el usuario.»**

Evidencia: `resultado-04.txt`, `falla-reproducida.txt`, `falla-reproducida.meta.json`, `cli-04.txt` y snapshot `s3/rondas/04-administradores/main.py`.

## Tres reflexiones técnicas del asistente

1. **¿En qué ronda se alejó más la predicción y por qué?** En las tres rondas, las predicciones principales coincidieron bastante con lo ejecutado; no sería fiel inventar un gran error de predicción. La ampliación menos prevista apareció en la ronda 3: se añadieron username obligatorio y rechazo de duplicados, aunque el pedido solo hablaba de una lista con email y contraseña. La discrepancia más clara ocurrió en el cierre: no se omitió el email como se temía; el defecto estuvo en el tipo del nuevo indicador de administrador. Se razonó sobre el flujo funcional y no se anticipó la coerción por truthiness.

2. **¿El resultado fue igual al del instructor y qué enseña pedir sin spec?** No se puede comparar: no hay ejecución ni captura del instructor disponible. Esta secuencia tampoco prueba por sí sola que dos agentes respondan distinto al mismo pedido. Sí muestra que el agente tomó decisiones no solicitadas —política, duplicados, estructura y significado de «opcional»— y que faltó un contrato de entrada para el nuevo rol. Esas decisiones deben volverse explícitas y comprobables antes de compartir el código como solución mantenible.

3. **Frase completada como reflexión técnica:** «Si yo tuviera que darle este código a otra persona mañana, tendría que explicarle la política de contraseñas, el tratamiento de duplicados, quién asigna el rol, que is_admin debe ser un booleano real y cómo distinguir una validación omitida de una contraseña válida, porque eso no está escrito en ningún lado». En esta frase, «no está escrito» significa que no existe un contrato explícito fuera de las decisiones implícitas del código. Esa es la materia que una spec posterior deberá fijar; no se añadió retrospectivamente a los pedidos del experimento.

## Reproducción y límites de entrega

Desde la raíz del proyecto: `uv run --project s3/experimento python s3/probar_ronda_01.py` (cambiar 01 por 02, 03 o 04). La segunda demostración del defecto se ejecuta con `uv run --project s3/experimento python s3/demostrar_falla.py` y debe fallar. La trazabilidad se verifica con `uv run --project s3/experimento python s3/verificar_trazabilidad.py`.

La evidencia textual es real. Los registros renderizados o el visor HTML no son capturas originales del aula. El coordinador debe distinguir capturas del visor, registros renderizados y cualquier captura original que Alberto aporte. Sigue sin estar disponible la comparación con el instructor ni una reflexión personal de Alberto. El PDF oficial y su entrega en AVAC los prepara el coordinador.

## Consulta posterior de la grabación

Después de completar el experimento se verificaron fotogramas y transcripción del instructor. La comparación actual está en `docs/p02/instructor-comparacion-v2.md` y las tres reflexiones actualizadas en `privado/p02-informe-datos-v2.json`. Las indicaciones anteriores de información no disponible describen el estado previo y se conservan sin retocar predicciones ni resultados. Hay contraste verificado de estructuras/salidas de las rondas1–3; no se confirmó el resultado del cierre del instructor.
