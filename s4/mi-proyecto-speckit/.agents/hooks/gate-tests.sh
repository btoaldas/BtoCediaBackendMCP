#!/bin/bash
# Hook Stop agy. Funciona desde .agents/ y desde cualquier cwd.
project_root="$(cd "$(dirname "$0")/../.." && pwd)" || {
  printf '%s\n' '{"decision":"continue","reason":"No se pudo resolver el proyecto para ejecutar pytest."}'
  exit 0
}
cd "$project_root" || exit 1
gate_run="$project_root/.qa-gate-runs/$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir -p "$gate_run" || {
  printf '%s\n' '{"decision":"continue","reason":"No se pudo guardar evidencia de la comprobación de tests."}'
  exit 0
}
if uv run pytest tests/ --tb=short -q > "$gate_run/pytest.log" 2>&1; then
  printf '0\n' > "$gate_run/exit-code.txt"
  printf '%s\n' '{}' | tee "$gate_run/decision.json"
else
  gate_status=$?
  printf '%s\n' "$gate_status" > "$gate_run/exit-code.txt"
  uv run python .agents/hooks/capturar-fallo.py "$gate_run" > "$gate_run/snapshot.log" 2>&1
  printf '%s\n' '{"decision":"continue","reason":"Hay tests fallando. No te detengas: corrige el código antes de terminar. La evidencia y fuentes del fallo están en .qa-gate-runs."}' | tee "$gate_run/decision.json"
fi
