#!/bin/bash
# Demostración reversible del hook pre-commit del Proyecto Integrador (Anexo: hooks).
# 1) Cambio en app/services/ con un test de services roto a propósito -> el commit se bloquea.
# 2) SECRET_KEY escrita en el código -> el commit se bloquea.
# 3) Sin los cambios de prueba el hook deja pasar. Todo se restaura al salir.
cd "$(dirname "$0")/../s9/proyecto-integrador" || exit 1
SERV=app/services/productos.py
TEST=tests/unit/test_services_productos.py
if [ -n "$(git status --porcelain -- "$SERV" "$TEST")" ]; then
  echo "Hay cambios sin commit en $SERV o $TEST: no se ejecuta la demo." >&2
  exit 1
fi
restaurar() { git reset -q; git checkout -q HEAD -- "$SERV" "$TEST"; }
trap restaurar EXIT

echo "== 1) Cambio en app/services/ y un test de services roto a propósito"
echo "# cambio de prueba para el hook" >> "$SERV"
printf '\n\ndef test_roto_a_proposito():\n    assert 1 == 2, "roto a propósito para probar el hook"\n' >> "$TEST"
git add "$SERV" "$TEST"
echo "== git commit -m 'prueba del hook'   (debe BLOQUEARSE)"
git commit -q -m "prueba del hook" 2>&1 | grep -E 'pre-commit|passed|failed|BLOQUEADO' | grep -v '^FAILED'
echo "   exit del commit: ${PIPESTATUS[0]}   commit creado: $(git log -1 --format=%s | grep -c 'prueba del hook') (0 = no)"
restaurar

echo "== 2) SECRET_KEY escrita en el código"
printf '\nSECRET_KEY = "%s"\n' "valor-de-prueba-no-real" >> "$SERV"
git add "$SERV"
echo "== git commit -m 'prueba del hook'   (debe BLOQUEARSE)"
git commit -q -m "prueba del hook" 2>&1 | grep -E 'BLOQUEADO|passed|failed'
echo "   exit del commit: ${PIPESTATUS[0]}   commit creado: $(git log -1 --format=%s | grep -c 'prueba del hook') (0 = no)"
restaurar

echo "== 3) Mismo cambio en services, sin test roto ni secreto: el hook deja pasar"
echo "# cambio de prueba para el hook" >> "$SERV"
git add "$SERV"
.git/hooks/pre-commit 2>&1 | grep -E 'pre-commit|passed|failed|BLOQUEADO'
echo "   exit del hook: ${PIPESTATUS[0]}  (0 = deja pasar)"
echo "== 4) Se descartan los cambios de prueba"
