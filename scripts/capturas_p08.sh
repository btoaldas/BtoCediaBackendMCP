#!/bin/bash
# Capturas reales de la Práctica 08 en ventanas de Terminal.app. Uso: capturas_p08.sh <carpeta_salida>
set -uo pipefail
OUT="$1"; mkdir -p "$OUT"
R=~/Developer/BtoCediaBackendMCP
P=$R/s9/proyecto-curso-speckit
T=$R/scripts/captura_terminal.sh
$T "$P" "$OUT/01-constitucion-y-skills.png" 112 24 'ls .agents/skills && grep -E "^### " .specify/memory/constitution.md'
$T "$P" "$OUT/02-clarify.png" 165 22 "sed -n '/^## Clarifications/,/^## User Scenarios/p' specs/001-control-gastos/spec.md | cut -c1-163"
$T "$P" "$OUT/03-historial-sdd.png" 125 30 'git log --oneline --reverse'
$T "$P" "$OUT/04-tests-referencia.png" 125 32 'for f in __init__.py test_gastos.py test_integracion_gastos.py test_api_gastos.py; do cmp -s tests/$f ../../s6-s8/proyecto-curso/tests/$f && echo "idéntico a S6-S8: tests/$f"; done; uv run pytest tests/test_gastos.py tests/test_integracion_gastos.py tests/test_api_gastos.py -v -p no:warnings | tail -12'
$T "$P" "$OUT/05-casos-4-y-5.png" 135 18 'uv run pytest tests/test_seguridad_gastos.py -v -p no:warnings | tail -7'
$T "$P" "$OUT/06-cobertura.png" 105 46 'uv run pytest --cov=app --cov-report=term-missing -q -p no:warnings | tail -37'
$T "$P" "$OUT/07-correccion-tasks.png" 168 40 "sed -n '/## Prompt enviado a agy/,/## Respuesta final de agy/p' ../../evidencia/p08/agy/10-tasks-reorganizar.md | cut -c1-166 | head -36"
$T "$P" "$OUT/08-correccion-mcp.png" 168 44 "sed -n '/## Prompt enviado a agy/,/## Respuesta final de agy/p' ../../evidencia/p08/agy/16-correcciones-mcp-y-fase7.md | cut -c1-166 | head -40"
$T "$P" "$OUT/09-subagentes.png" 150 30 'python3 ../../scripts/resumen_subagentes.py ../../evidencia/p08/agy'
$T "$P" "$OUT/10-hook-bloquea-y-pasa.png" 125 24 'bash ../../scripts/demo_hook_p08.sh'
echo listo
