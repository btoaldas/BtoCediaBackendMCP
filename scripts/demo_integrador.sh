#!/bin/bash
# Levanta el Proyecto Integrador para las capturas en vivo, con base SQLite temporal y datos sintéticos.
# Uso: demo_integrador.sh <puerto> <archivo_sqlite>
# Deja en /tmp/cedia49098/demo-int.env (permisos 600) las claves y tokens de los dos usuarios sintéticos:
# nunca se imprimen y el archivo vive fuera de cualquier repositorio.
set -euo pipefail
PUERTO="$1"; DB="$2"
P=~/Developer/BtoCediaBackendMCP/s9/proyecto-integrador
ENVF=/tmp/cedia49098/demo-int.env
cd "$P"
if [ -e "$DB" ]; then echo "La base $DB ya existe: elija otra ruta." >&2; exit 1; fi
export DATABASE_URL="sqlite:///$DB"
uv run alembic upgrade head >/dev/null 2>&1
nohup uv run uvicorn app.main:app --port "$PUERTO" > "/tmp/cedia49098/demo-int-$PUERTO.log" 2>&1 &
for _ in $(seq 1 30); do curl -sf "http://127.0.0.1:$PUERTO/docs" >/dev/null && break; sleep 0.5; done
B="http://127.0.0.1:$PUERTO"
CA=$(openssl rand -hex 8); CB=$(openssl rand -hex 8)
alta() { curl -sf -o /dev/null -X POST "$B/usuarios/" -H 'Content-Type: application/json' -d "{\"email\":\"$1\",\"password\":\"$2\"}"; }
token() { curl -sf -X POST "$B/usuarios/token" -d "username=$1&password=$2" | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])'; }
alta bodega@ejemplo.com "$CA"; alta otra.bodega@ejemplo.com "$CB"
TA=$(token bodega@ejemplo.com "$CA"); TB=$(token otra.bodega@ejemplo.com "$CB")
crear() { curl -sf -o /dev/null -X POST "$B/productos/" -H "Authorization: Bearer $1" -H 'Content-Type: application/json' -d "$2"; }
crear "$TB" '{"nombre":"Cinta adhesiva","cantidad":8,"cantidad_minima":2}'
crear "$TA" '{"nombre":"Papel bond A4","cantidad":40,"cantidad_minima":10}'
crear "$TA" '{"nombre":"Grapas 26/6","cantidad":3,"cantidad_minima":5}'
umask 077
printf 'CLAVE_SWAGGER=%s\nCLAVE_B=%s\nTOKEN_A=%s\nTOKEN_B=%s\n' "$CA" "$CB" "$TA" "$TB" > "$ENVF"
echo "servidor en $B (base $DB); usuarios sintéticos bodega@ejemplo.com y otra.bodega@ejemplo.com; secretos en $ENVF"
