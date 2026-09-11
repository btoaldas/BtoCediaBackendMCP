---
name: qa-orchestrate
description: Ejecuta el flujo completo de calidad invocando en orden a tester-agent, security-agent y report-agent, sin pedir confirmación entre cada uno.
---
# Instrucciones
1. Verifica que exista `specs/*/spec.md`. Si falta, detente y pide que se corra Spec Kit primero.
2. Invoca al agente tester-agent (su propia tarea vive en su `agent.md`). Espera a que termine por completo.
3. Invoca al agente security-agent (su propia tarea vive en su `agent.md`). Espera a que termine por completo.
4. Invoca al agente report-agent (su propia tarea vive en su `agent.md`).
5. Presenta al usuario el veredicto final, con un resumen de 1 línea de qué hizo cada agente en el camino.

No pidas confirmación entre fase y fase — este es un flujo automático de punta a punta. Si `agy` te pide aprobar el permiso de invocación de cada agente, apruébalo y sigue.


## Compatibilidad verificada con CLI 1.2.0

Antes de invocar los agentes, garantiza su capacidad real de ejecutar las skills.
Si los roles cargados desde agent.md carecen de ejecución, usa la herramienta
nativa `define_subagent`/`DefineSubagent` para definir alias transitorios
`tester-agent-native`, `security-agent-native`, `report-agent-native` con el
contenido completo de sus respectivos agent.md como system_prompt y
`enable_write_tools=true`. No agregues campos de frontmatter no comprobados ni
cambies permisos globales. Conserva los mismos roles y la misma secuencia.

Si un subagente espera permiso, espera al operador; no lo termines ni atribuyas
al subagente una ejecución del principal. Las aprobaciones acotadas por acción
son compatibles con el flujo automático y pueden resolverse en la TUI con Ctrl+K.
Exige resultados de comandos reales, no solo lectura de informes anteriores.
Los tests por capa deben producir JSON separados en un directorio nuevo de
`.qa-runs/` para conservar conteos, exit codes y atribución. El reportador ya crea
su propia corrida única. Si hubo correcciones, repite las verificaciones afectadas
antes del reporte final, conservando la evidencia roja y los informes previos.

Esta adaptación deriva de una ejecución real documentada en
`docs/p03-p04/compatibilidad-agy-1.2.0.md` desde la raíz del repositorio del curso.
