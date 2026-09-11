# Curso Backend y MCP en Python

Proyecto de formación personal y laboratorio. Objetivo: completar las prácticas publicadas con código ejecutado, evidencia trazable e informes fieles a las guías. No constituye un servicio institucional ni productivo.

## Alcance y estado

Prácticas 1 a 7, prueba y seguimiento de entregas del curso MOD2 de agosto de 2026. Estado: recuperación de actividades. Mantener separados original del docente, desarrollo y evidencia. No fabricar asistencia, predicciones personales, ejecuciones, capturas, calificaciones ni aceptación docente.

## Autoridad y seguridad

El usuario autoriza crear y resolver las prácticas, reunir materiales, entregar lo solicitado y guardar copia en Obsidian. Antes de publicar un repositorio nuevo falta acordar propietario y visibilidad. No crear cuentas, comprar, aceptar términos, cambiar credenciales, desplegar o borrar. Anunciar cambios; no sobrescribir datos previos ni limpiar archivos sin aprobación. Secretos solo por variables de entorno; nunca en Git, logs o informes. Datos de laboratorio sintéticos.

## Arquitectura y trabajo compartido

Python 3.12 y uv. `s02` contiene API Gemini y memoria, `s3` el experimento de prompts sin especificación, `s4` las versiones manual y Spec Kit y su QA. `informes` conserva entregables; `materiales` originales del docente fuera de Git; `privado` evidencias con identificación fuera de Git. Cada trabajador tiene propiedad exclusiva asignada. No revertir cambios ajenos. Git local main, sin remoto por ahora. No commits globales ni git add indiscriminado.

## Validación y evidencia

Pruebas unitarias, integración y ejecución CLI según cada guía. Los mocks se identifican como simulación y no reemplazan una llamada real exigida. Capturas deben provenir de ejecuciones reales. Entrega AVAC exige estado persistente enviado, nombre de archivo y revisión final. Calificación docente y emisión certificado son estados distintos.

## Reversibilidad

Añadir versiones y conservar originales. Ningún rollback elimina datos sin aprobación. No producción ni despliegue.

## Economía de contexto

Grafo de código primero para consultas estructurales, luego funciones concretas. No volcar árboles completos ni releer guías ya resumidas. Documentar cambios en bitácora y roadmap.
