#!/bin/bash
# Levanta el Proyecto Integrador en un puerto libre con una base SQLite nueva, ejecuta una verificación
# en vivo y detiene el servidor al terminar. Uso: vivo_integrador.sh e2e|stdio <puerto>
set -uo pipefail
MODO="$1"; PUERTO="$2"
P="$(cd "$(dirname "$0")/.." && pwd)/s9/proyecto-integrador"
DB="/tmp/cedia49098/vivo-$MODO-$(date +%H%M%S).db"
cd "$P" || exit 1
export DATABASE_URL="sqlite:///$DB"
uv run alembic upgrade head >/dev/null 2>&1
uv run uvicorn app.main:app --port "$PUERTO" >/dev/null 2>&1 &
SERVIDOR=$!
trap 'kill $SERVIDOR 2>/dev/null' EXIT
for _ in $(seq 1 40); do curl -sf "http://127.0.0.1:$PUERTO/docs" >/dev/null && break; sleep 0.5; done
echo "== servidor: uvicorn app.main:app en 127.0.0.1:$PUERTO · base nueva con alembic upgrade head"
if [ "$MODO" = "e2e" ]; then
  uv run python "$P/../../scripts/e2e_inventario.py" "http://127.0.0.1:$PUERTO"
else
  E="stdio-$(openssl rand -hex 3)@ejemplo.com"; K=$(openssl rand -hex 10)
  curl -sf -o /dev/null -X POST "http://127.0.0.1:$PUERTO/usuarios/" -H 'Content-Type: application/json' -d "{\"email\":\"$E\",\"password\":\"$K\"}"
  MCP_ACCESS_TOKEN=$(curl -sf -X POST "http://127.0.0.1:$PUERTO/usuarios/token" -d "username=$E&password=$K" | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
  export MCP_ACCESS_TOKEN
  echo "== usuario sintético $E; su JWT va en MCP_ACCESS_TOKEN (no se imprime)"
  echo "== uv run mcp run app/mcp/server.py (stdio) con el JWT:"
  uv run python "$P/../../scripts/stdio_inventario.py" 2>/dev/null
  echo "== el mismo servidor por stdio con MCP_ACCESS_TOKEN vacío:"
  uv run python "$P/../../scripts/stdio_inventario.py" --sin-token 2>/dev/null
  echo "== dueño del producto creado por stdio (consulta directa a la base):"
  sqlite3 "$DB" "select p.nombre || ' -> ' || u.email from productos p join usuarios u on u.id = p.usuario_id;"
fi
