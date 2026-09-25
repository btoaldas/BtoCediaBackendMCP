#!/bin/bash
# Capturas reales del Proyecto Integrador en ventanas de Terminal.app. Uso: capturas_integrador.sh <carpeta_salida> [n...]
set -uo pipefail
OUT="$1"; shift; mkdir -p "$OUT"
R=~/Developer/BtoCediaBackendMCP
P=$R/s9/proyecto-integrador
T=$R/scripts/captura_terminal.sh
A=../../evidencia/integrador/agy
SEL=("$@")
toca() { [ ${#SEL[@]} -eq 0 ] && return 0; for s in "${SEL[@]}"; do [ "$s" = "$1" ] && return 0; done; return 1; }
prompt_de() { echo "sed -n '/## Prompt enviado a agy/,/## Respuesta final de agy/p' $A/$1 | grep -v '^\`\`\`' | fold -s -w 166 | head -$2"; }
toca 01 && $T "$P" "$OUT/01-constitucion-y-skills.png" 112 26 'ls .agents/skills && grep -E "^### " .specify/memory/constitution.md'
toca 02 && $T "$P" "$OUT/02-clarify.png" 168 24 "sed -n '/^## Clarifications/,/^## User Scenarios/p' specs/001-inventario-insumos/spec.md | fold -s -w 166 | head -22"
toca 03 && $T "$P" "$OUT/03-historial-sdd.png" 140 16 'git --no-pager log --oneline --reverse'
toca 04 && $T "$P" "$OUT/04-correccion-spec.png" 168 16 "$(prompt_de 03-specify-restaurar-contratos.md 14)"
toca 05 && $T "$P" "$OUT/05-correccion-analyze.png" 168 30 "$(prompt_de 09-analyze-revision-manual.md 28)"
toca 06 && $T "$P" "$OUT/06-correccion-revision.png" 168 46 "$(prompt_de 16-correccion-revision-stdio-contrato-cobertura.md 44)"
toca 07 && $T "$P" "$OUT/07-rojo-verde.png" 150 34 'echo "== ROJO: pruebas nuevas contra el código de 48e540f (antes de corregir)"; cat ../../evidencia/integrador/revision/rojo-pruebas-revision-contra-48e540f.txt ../../evidencia/integrador/revision/rojo-pruebas-revision-2-contra-48e540f.txt | grep -E "^FAILED|passed|failed" | cut -c1-148; echo; echo "== VERDE: las mismas pruebas sobre el código corregido (HEAD)"; uv run pytest tests/mcp/test_stdio.py tests/mcp/test_revision_humana.py tests/mcp/test_identidad_transporte.py tests/test_portabilidad.py tests/unit/test_schemas_producto.py tests/api/test_api_productos.py -q -p no:warnings | tail -1'
toca 08 && $T "$P" "$OUT/08-subagentes.png" 150 16 "python3 ../../scripts/resumen_subagentes.py $A"
toca 09 && $T "$P" "$OUT/09-tests-por-regla.png" 130 40 'uv run pytest tests/unit/test_services_productos.py -v -p no:warnings | grep -E "PASSED|FAILED|passed" | sed -E "s/ +\[ *[0-9]+%\]//"'
toca 10 && $T "$P" "$OUT/10-integracion-bd-real.png" 130 22 'uv run pytest tests/integration -v -p no:warnings | grep -E "PASSED|FAILED|passed" | sed -E "s/ +\[ *[0-9]+%\]//"'
toca 11 && $T "$P" "$OUT/11-cobertura.png" 105 50 'uv run pytest --cov=app --cov-report=term-missing -q -p no:warnings | tail -44'
toca 12 && $T "$P" "$OUT/12-hook.png" 125 24 'bash ../../scripts/demo_hook_integrador.sh'
toca 13 && $T "$P" "$OUT/13-e2e-en-vivo.png" 150 50 'bash ../../scripts/vivo_integrador.sh e2e 8044'
toca 14 && $T "$P" "$OUT/14-stdio-en-vivo.png" 160 16 'bash ../../scripts/vivo_integrador.sh stdio 8045'
echo listo
