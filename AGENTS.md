# Curso Backend y MCP en Python

Proyecto de formación personal y laboratorio. Objetivo: completar las prácticas publicadas con código ejecutado, evidencia trazable e informes fieles a las guías. No constituye un servicio institucional ni productivo.

## Alcance y estado

Prácticas 1 a 7, prueba y seguimiento de entregas del curso MOD2 de agosto de 2026. Estado: recuperación de actividades. Mantener separados original del docente, desarrollo y evidencia. No fabricar asistencia, predicciones personales, ejecuciones, capturas, calificaciones ni aceptación docente.

## Autoridad y seguridad

El usuario autoriza crear y resolver las prácticas, reunir materiales, entregar lo solicitado y guardar copia en Obsidian. Autorizó publicar código y evidencia revisados en GitHub público btoaldas/BtoCediaBackendMCP, rama main, incluyendo P3/P4 tras verificación. Los informes identificados y los materiales originales del docente quedan fuera. La autenticación de agy, sus términos sin cesión de interacciones y el permiso de archivos de la extensión del navegador recibieron autorización específica. Estas decisiones no autorizan otras cuentas, compras, términos, credenciales, despliegues o borrados. Anunciar cambios; preservar versiones previas y no limpiar archivos sin aprobación. Secretos solo por variables de entorno; nunca en Git, logs o informes. Datos de laboratorio sintéticos.

## Arquitectura y trabajo compartido

Python 3.12 y uv. `s02` contiene API Gemini y memoria, `s3` el experimento de prompts sin especificación, `s4` las versiones manual y Spec Kit y su QA. `informes` conserva entregables; `materiales` originales del docente fuera de Git; `privado` evidencias con identificación fuera de Git. Cada trabajador tiene propiedad exclusiva asignada. No revertir cambios ajenos. Git local main y remoto público autorizado. Publicar únicamente archivos revisados mediante una selección explícita; no usar git add indiscriminado.

## Validación y evidencia

Pruebas unitarias, integración y ejecución CLI según cada guía. Los mocks se identifican como simulación y no reemplazan una llamada real exigida. Capturas deben provenir de ejecuciones reales. Entrega AVAC exige estado persistente enviado, nombre de archivo y revisión final. Calificación docente y emisión certificado son estados distintos.

## Reversibilidad

Añadir versiones y conservar originales. Ningún rollback elimina datos sin aprobación. No producción ni despliegue.

## Economía de contexto

Grafo de código primero para consultas estructurales, luego funciones concretas. No volcar árboles completos ni releer guías ya resumidas. Documentar cambios en bitácora y roadmap.

<!-- skill-anexos:navegacion-e2e-coherencia-20261025:begin -->
## Navegación E2E y acceso autorizado — regla vigente (2026-10-25)

Esta regla se aplica automáticamente a la navegación web y a las pruebas E2E web de este proyecto y sus agentes, skills y subdirectorios. En este ámbito prevalece sobre instrucciones anteriores incompatibles, como exigir un navegador visible, un perfil personal, una ruta fija de caché de otro sistema o el tecleo manual de credenciales disponibles.

- Aplicar los skills `playwright` y `chromium-headless`: Chromium interno de Playwright en modo headless, sin abrir ventanas ni depender de Chrome del usuario o de una extensión. Reutilizar el runtime, la configuración y las pruebas del proyecto; resolver el ejecutable con la API y comprobar los parámetros efectivos. Las pruebas nativas de escritorio o móvil conservan su herramienta específica. Si el usuario solicita expresamente su Chrome o su sesión, aplicar `chrome-browser` y los permisos de esa superficie.
- Si el usuario autoriza expresamente cuenta, destino y tarea autenticada, aplicar `acceso-web-autorizado` automáticamente: recuperar e introducir internamente la credencial pertinente de Obsidian, Llavero o la fuente local autorizada, o la que proporcione el usuario. No exigir invocación manual del skill ni volver a pedir su tecleo. Esta cláusula por sí sola no autoriza entrar a cuentas.
- Comprobar origen y cuenta antes de introducir y enviar credenciales; respetar MFA, CAPTCHA y permisos. No eludir una denegación. Máximo dos intentos; no exponer secretos en scripts, argumentos, registros, snapshots, capturas, trazas, repositorios ni informes. Para accesos reales prevalece la fuente autorizada vigente sobre literales heredados.
- El acceso conserva las autorizaciones específicas para envíos, publicaciones, firmas, pagos, borrados y cambios de datos o producción. Cerrar solo la sesión propia. La instalación global no demuestra que este proyecto pase sus pruebas: en otro equipo, cloud o CI comprobar skills, dependencias y navegador por separado; no copiar perfiles ni almacenes de credenciales por inferencia.

Para seleccionar Chromium completo, usar `channel="chromium"` con headless activo (por ejemplo, `headless=True` en Python o `headless: true` en JavaScript). El agente realiza internamente la navegación y las capturas de evidencia cuando la herramienta y el alcance estén autorizados; solicita intervención solo ante una autorización que falte, MFA, CAPTCHA, permisos o un recurso inaccesible. Esta precisión prevalece sobre ejemplos anteriores que deleguen al usuario abrir y capturar una página que el agente puede comprobar dentro del alcance autorizado.

Los procedimientos específicos de grabación o demostración de una interfaz solicitada conservan sus herramientas y permisos. Las comprobaciones internas y E2E web de esos repositorios siguen el carril anterior; los motores productivos existentes conservan su arquitectura.

<!-- skill-anexos:navegacion-e2e-coherencia-20261025:end -->
