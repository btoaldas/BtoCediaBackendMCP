# Informe técnico de recuperación — práctica 2

**Vibe Coding: El Experimento Guiado.** Sesión 3. Ejecución local: 10 de septiembre de 2026. Estado: borrador para revisión del estudiante y composición en la plantilla oficial.

Se ejecutaron cuatro pedidos reales con agy autenticado y Python 3.12.13. Cada predicción fue registrada antes de la llamada y cada snapshot coincide byte por byte con el código recibido. Por una limitación de permisos del modo headless, los mensajes incluyeron una nota operativa para devolver código sin herramientas; Codex guardó y probó las respuestas. Las predicciones y reflexiones son del asistente, sin atribución retrospectiva al estudiante.

## Resultado

Las rondas 1–3 implementaron contraseñas, email y una lista de dos usuarios. Los casos exigidos fueron ejecutados y las respuestas anteriores se compararon al ampliar el programa. El generador incorporó decisiones no pedidas: longitud máxima, patrones prohibidos, username obligatorio y rechazo de correos duplicados.

El cierre añadió `is_admin` y una opción para exigir la contraseña a administradores. La falla observada consiste en aceptar `is_admin="false"` como indicador verdadero: la contraseña `12345` es inválida directamente, pero pasa dentro del usuario. La reproducción desde JSON y validación por lote termina con AssertionError (exit 1). La falla queda intencionalmente preservada: documentarla forma parte de la práctica.

La mitigación para una implementación posterior sería validar tipos al ingresar datos, rechazar indicadores de rol mal formados, obtener el rol de una fuente de autoridad y distinguir un estado «omitido» de «válido». No se aplicó esa corrección a los snapshots del experimento ni se afirma una vulnerabilidad desplegada.

## Matriz de requisitos

| Requisito de la guía | Estado técnico | Evidencia |
|---|---|---|
| Python 3.12, uv y agy autenticado | Comprobado | entorno.json, respuestas reales agy |
| Predicción antes de cada resultado | Comprobado, autor asistente | prediccion-01..04.json, trazabilidad.txt |
| Ronda 1: 12345, password y vacío | Comprobado | resultado-01.txt, registro-01.png |
| Ronda 2: email válido, ana@ y vacío | Comprobado | resultado-02.txt, registro-02.png |
| Ronda 3: dos usuarios y lista completa | Comprobado | resultado-03.txt, registro-03.png |
| Cierre: pedido administradores y comportamiento inconsistente | Comprobado por dos vías | resultado-04.txt, falla-reproducida.txt, registro-04.png |
| Capturas de al menos dos rondas y cierre | Se aportan registros renderizados reales; captura original de UI pendiente | registro-01..04.png, visor-evidencia.html |
| Tres reflexiones | Reflexión técnica del asistente disponible; revisión personal pendiente | s3/notas.md |
| Comparación con instructor | No disponible; no inventada | límite declarado en notas |
| Repositorio de código | No requerido por esta guía | originales locales conservados para trazabilidad |
| PDF oficial y entrega AVAC | A cargo del coordinador | privado/p02-informe-datos-v1.json |

## Archivos para el coordinador

- `s3/notas.md`: notas y tres reflexiones completas.
- `s3/rondas/01-contrasenas` a `04-administradores`: evolución exacta.
- `evidencia/p02/resultado-01.txt` a `resultado-04.txt`: ejecución de los casos de la guía.
- `evidencia/p02/cli-01.txt` a `cli-04.txt`: segundo ángulo desde la CLI generada.
- `evidencia/p02/falla-reproducida.txt`: contraejemplo desde JSON, con fallo esperado.
- `evidencia/p02/trazabilidad.txt`: predicciones previas, pedidos literales y hashes verificados.
- `evidencia/p02/registro-01.png` a `registro-04.png`: registros renderizados honestamente etiquetados, con `.txt` fuente.
- `evidencia/p02/visor-evidencia.html`: visor local de esos registros.
- `privado/p02-informe-datos-v1.json`: insumo conforme contrato del generador; borrador.

Los logs `*provider.log` y el estado interno `.antigravitycli` no son fuentes para los informes y deben permanecer fuera de Git/entrega. El nombre del estudiante se conserva únicamente en el insumo privado, según la separación del proyecto.

## Copias publicables saneadas

La falla con traceback se conserva original y tiene una copia en `evidencia/p02/publicable/falla-reproducida.txt`. El prefijo absoluto se sustituyó por `<PROJECT_ROOT>`; `manifiesto-saneamiento.json` registra ambos hashes. `publicable/rondas-trazabilidad.json` conserva tiempos, pedidos y hashes de las cuatro respuestas sin rutas privadas. No se alteró ningún snapshot.

## Actualización posterior — versión2

Se añadieron tres capturas reales del visor (rondas1,2 y cierre) y una comparación posterior con la grabación. La fuente vigente para esa comparación es `docs/p02/instructor-comparacion-v2.md`; corrige el alcance de la nota v1 sobre el vacío distinguiendo narración y salida de CLI. El insumo vigente es `privado/p02-informe-datos-v2.json`, con clase3, siete evidencias y tres reflexiones asistidas. Las notas y capturas anteriores se preservan como estado histórico, sin cambiar predicciones.
