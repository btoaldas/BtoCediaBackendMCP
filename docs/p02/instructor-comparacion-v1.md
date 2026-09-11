# Contraste posterior con la grabación de la sesión 3

Consulta posterior a las cuatro rondas propias. No modifica retroactivamente las predicciones ni el JSON v1.

Fuente: [VIDEO SESIÓN 3: 31 DE AGOSTO, AVAC](https://cursos.cedia.org.ec/mod/page/view.php?id=48522), reproductor Vimeo 1223032852. Consulta mediante pestaña propia autenticada de Edge; sin extraer cookies ni realizar solicitudes HTTP fuera del navegador. Fecha local de consulta: 10 de septiembre de 2026.

## Hechos comprobados

- **36:18–37:17:** el docente presenta un ejemplo de especificación con mínimo 12 caracteres. Ese tramo pertenece a la explicación de spec, no al resultado generado del experimento; no debe confundirse con la ronda 1.
- **1:07:04:** la transcripción ubica el pedido literal del validador de contraseñas.
- **1:10:08–1:10:18:** el instructor explica que el agente generó el validador y pruebas por iniciativa propia.
- **1:11:32, fotograma pausado y ampliado:** el reporte visible del instructor muestra una contraseña válida, fortaleza «Muy Fuerte (100/100)» y entropía 111.4 bits. Sus nueve comprobaciones visibles incluyen mínimo 8, máximo 128, mayúsculas, minúsculas, números, símbolos, ausencia de espacios, variedad suficiente (16 caracteres únicos) y no ser una contraseña común conocida.
- **1:12:38–1:12:48, transcripción:** el instructor ejecuta el caso vacío y explica que el validador lo considera incorrecto. El fotograma de ese caso todavía no fue inspeccionado al crear esta nota.

## Comparación acotada

El código propio de la ronda 1 coincide con el instructor en mínimo 8, máximo 128, clases de caracteres y rechazo de espacios. El resultado propio usa una dataclass con is_valid, errors y una etiqueta strength; no devuelve puntuación sobre 100 ni entropía en bits. Por tanto, el formato de resultado no fue idéntico, aunque varias reglas coincidieron.

No se afirma igualdad completa de políticas: la lista de patrones del código propio no se ha comparado con la lista interna del instructor. La diversidad de caracteres se usa en el cálculo propio de fuerza, pero no es una regla que por sí sola invalide la contraseña. La comparación de email, usuarios y administradores sigue en revisión.

La evidencia visual fue inspeccionada en vivo mediante CUA. No se ha guardado aquí una captura de ese fotograma ni se afirma haber recuperado el código fuente del instructor.
