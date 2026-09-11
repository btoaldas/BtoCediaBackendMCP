# Práctica 1 Resultados de ejecución y límites

Fecha de ejecución local: 10 de septiembre de 2026. Python 3.12.13, google-genai 2.23.0, modelo gemini-2.5-flash. Implementación y revisión asistidas por Codex; llamadas de demostración realizadas al proveedor real.

## Resultado verificado

Ocho intercambios reales conservaron Alex y verde desde el primer turno hasta el octavo. El último resultado fue «Te llamas Alex y tu color favorito es el verde». El historial terminó con 16 entradas alternadas y el proceso salió con código 0. Los totales de tokens registrados por turno fueron 82, 159, 222, 296, 333, 409, 483 y 508. Son consumos por solicitud, no tamaños incrementales independientes: cada llamada reenvía historia.

Sin reenvío de historial, el proveedor no recordó Valeria en la segunda solicitud. Las ejecuciones de temperatura 0.1 y 1.3 produjeron dos respuestas diferentes sobre var; esta muestra no demuestra estadísticamente cómo cambia la variabilidad.

Se conservaron dos ensayos reales de tasa: 20 pedidos mínimos de OK sin historial, y otros 20 pedidos consecutivos de conteo con historial conforme al paso 9. Ninguno produjo 429; todas las respuestas concluyeron con STOP. Falta la evidencia del error real que pide la guía. El comportamiento de retry se verifica con dobles de prueba claramente identificados, sin presentar esos errores sintéticos como respuestas del proveedor.

## Interpretación crítica del transcript

La demostración prueba memoria de contexto, no exactitud general del modelo. Se preservó el transcript sin corregirlo retrospectivamente. Contiene estas imprecisiones:

- Turno 3: la explicación de un entero demasiado grande para int no corresponde a Python. Los enteros de Python tienen precisión ilimitada, sujeta a memoria disponible; una fracción como 3.5 sí requiere otra representación si se quiere conservar su parte fraccionaria. [Documentación oficial Python](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex).
- Turno 4: uv init crea un proyecto y sus archivos iniciales, no es el comando dedicado a crear un entorno virtual. uv venv crea el entorno y uv sync puede crearlo al sincronizar dependencias. [Documentación oficial uv init](https://docs.astral.sh/uv/concepts/projects/init/).
- Turno 5: la respuesta define token léxico de un programa; el contexto de la actividad requería la unidad en que el modelo procesa entrada y salida. La pregunta debe precisar «token de un modelo de lenguaje» para evitar esa ambigüedad.

## Matriz de entrega

| Requisito | Estado | Evidencia |
|---|---|---|
| Python 3.12, uv y dependencias | Cumplido | pyproject y uv.lock en s02 |
| Parámetros y conteo explícitos | Cumplido | gemini_client.py, logs de uso y test de configuración |
| Ocho turnos y recuerdo inicial | Cumplido con proveedor real | memoria-20260910.txt y JSON |
| Ventana elegida y justificada | Cumplido | README s02 y pruebas de ventana de diez pares |
| Manejo separado de 429, otros4xx y5xx | Cumplido en pruebas deterministas | tests/test_memory_and_retry.py |
| Captura de 429 real | Pendiente | Ninguno observado en dos ensayos acotados |
| Repositorio accesible y push | Pendiente | Solo Git local al momento de este documento |
| PDF y recepción AVAC | Pendiente | Preparación local, no envío confirmado |

Los registros completos están en entregas/s02/evidencia. No se almacenó ninguna clave real en el proyecto. La evidencia original no contiene datos de alumnos ni conversaciones personales.
