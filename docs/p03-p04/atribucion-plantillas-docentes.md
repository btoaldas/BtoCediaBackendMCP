# Atribución de las plantillas docentes de P4

Las siete skills QA y los tres archivos de agente de este ejercicio proceden
de la **Guía Práctica — Pruebas, Cobertura y Seguridad (con Skills, Agentes y
Hooks)**, sesión 5 del curso **Programación de Backend y MCP en Python para IA
Generativa**, disponible en el AVAC de CEDIA. Se reconoce esa procedencia; no se
atribuyen estas plantillas a una creación original del estudiante o de Codex.
No se inventa un titular personal que no conste en la fuente.

## Base factual de su inclusión en el entregable

La sección final de la guía enumera estos archivos dentro de `.agents/`, junto
con las pruebas, el hook y el reporte, y pide: **«Repositorio con todo lo
anterior»**. Se incluyen aquí para reproducir ese entregable específico del
curso. Esta instrucción de uso académico no se presenta como una licencia
abierta general ni como autorización de redistribución para otros fines.

| Archivos bajo `s4/mi-proyecto-speckit/.agents/` | Procedencia y adaptación |
|---|---|
| `skills/qa-unit/SKILL.md` | Plantilla docente conservada |
| `skills/qa-integration/SKILL.md` | Plantilla docente conservada |
| `skills/qa-e2e/SKILL.md` | Plantilla docente conservada |
| `skills/qa-coverage/SKILL.md` | Plantilla docente conservada |
| `skills/qa-security/SKILL.md` | Plantilla docente conservada |
| `skills/qa-report/SKILL.md` | Plantilla docente conservada |
| `skills/qa-orchestrate/SKILL.md` | Base docente; se añadió una sección de compatibilidad comprobada con Antigravity CLI 1.2.0 |
| `agents/tester-agent/agent.md` | Plantilla docente conservada |
| `agents/security-agent/agent.md` | Plantilla docente conservada |
| `agents/report-agent/agent.md` | Plantilla docente conservada |

La comparación directa con la guía confirmó que los seis skills QA sin
ampliación y los tres archivos de agente conservan sus bloques completos.
`qa-orchestrate` conserva la base y añade la adaptación descrita en
[compatibilidad-agy-1.2.0.md](compatibilidad-agy-1.2.0.md), basada en definiciones
nativas transitorias y permisos por acción; no inventa un campo persistente de
frontmatter ni cambia la atribución de la plantilla base.

## Separación de licencias y otros archivos

**No se ha identificado una licencia abierta para estas plantillas docentes y
no se les asigna MIT.** La licencia MIT incluida en el repositorio corresponde
a GitHub Spec Kit y a sus componentes identificados, no a todo el laboratorio,
a las plantillas docentes ni a las evidencias. Los avisos generales están en
[THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

La guía completa, las grabaciones y el script docente original
`generar_reporte_guia_original.py` se preservan localmente y quedan fuera de la
publicación. El reportador ejecutable `generar_reporte.py` fue implementado por
Codex con ajustes deterministas de validación, integridad y escape; conserva la
finalidad del ejercicio y su procedencia se explica en
[ajustes-qa.md](ajustes-qa.md). Tampoco se le atribuye automáticamente MIT.

La copia local de referencia es `materiales/practica-04.md`, omitida del paquete
público. Su SHA-256 al revisar esta atribución es
`2ce94d151f0ff05d170945aebd7763de9cf6843f7dd2cba87c22011abab2f61a`.
Ese hash identifica la fuente contrastada; no acredita por sí mismo una licencia.
