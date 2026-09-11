# Conversor de temperatura — laboratorio de formación

Trabajar exclusivamente en este directorio, identificado por `.specify/`.
Leer las skills de `.agents/skills/` y agentes de `.agents/agents/` de aquí.
No buscar instrucciones, archivos ni credenciales en carpetas personales o
hermanas. No se necesitan servicios externos ni datos reales.

La fuente funcional es `specs/001-conversor-temperatura/spec.md`; usar sus
Acceptance Scenarios, Edge Cases y FR. El plan separa dominio, CLI y pruebas.
Python 3.12 + uv. No cambiar ramas, no commits, remotos ni pushes automáticos.
No borrar archivos. Conservar evidencias previas y registrar nuevas corridas
con fechas únicas. Los snapshots de fallos deben quedar aislados.

Para pytest se exigen pruebas unitarias, integración directa en memoria y e2e
con procesos reales. No llamar integración a un subprocess. No añadir tests de
negocio inventados fuera de la spec. Reportes deben rechazar errores de
recolección, cero tests o salidas anteriores. No imprimir secretos.

La constitución de Spec Kit sigue siendo una plantilla de fábrica; sus ejemplos
no constituyen decisiones de gobernanza ratificadas. Los límites reales son
los del laboratorio y el contrato funcional escrito.
