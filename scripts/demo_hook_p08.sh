#!/bin/bash
# Demostración reversible del hook pre-commit de la Práctica 08 (Anexo de la guía).
# Toca app/services/ y rompe a propósito un test propio de services (nunca los copiados de S6-S8),
# intenta el commit (debe bloquearse), corrige el test, vuelve a ejecutar el hook y restaura todo.
cd "$(dirname "$0")/../s9/proyecto-curso-speckit" || exit 1
restaurar() { git reset -q; git checkout -q -- app/services/gastos.py tests/test_services_usuarios.py; }
trap restaurar EXIT
echo "== 1) Cambio en app/services/ y un test de services roto a propósito"
echo "# cambio de prueba para el hook" >> app/services/gastos.py
printf '\n\ndef test_roto_a_proposito():\n    assert 1 == 2, "roto a propósito para probar el hook"\n' >> tests/test_services_usuarios.py
git add app/services/gastos.py tests/test_services_usuarios.py
echo "== 2) git commit -m 'prueba del hook'   (debe BLOQUEARSE)"
git commit -q -m "prueba del hook" 2>&1 | grep -E 'pre-commit|passed|failed|BLOQUEADO|FAILED' 
echo "   exit del commit: ${PIPESTATUS[0]}"
echo "   commit creado?: $(git log -1 --format=%s | grep -c 'prueba del hook') (0 = no)"
echo "== 3) Se corrige el test y se ejecuta el hook sobre el mismo cambio en services"
git checkout -q HEAD -- tests/test_services_usuarios.py && git add tests/test_services_usuarios.py
.git/hooks/pre-commit 2>&1 | grep -E 'pre-commit|passed|failed|BLOQUEADO'
echo "   exit del hook: ${PIPESTATUS[0]}  (0 = deja pasar)"
echo "== 4) Se descarta el cambio de prueba"
