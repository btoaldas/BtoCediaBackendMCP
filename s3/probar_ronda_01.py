"""Casos ejecutados sobre el código exacto generado en la primera ronda."""
from dataclasses import asdict
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys

path = Path(__file__).parent / "rondas/01-contrasenas/main.py"
spec = importlib.util.spec_from_file_location("ronda_01", path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

print("RONDA 1 — predicción previa en evidencia/p02/prediccion-01.json")
print("EJECUCIÓN UTC:", datetime.now(timezone.utc).isoformat())
print("POLÍTICA REAL:", json.dumps(asdict(module.PasswordPolicy()), ensure_ascii=False))
for password in ["12345", "password", "", "Ab3!xy7", "Ab3!xy7Z", "Password1!"]:
    result = module.validate_password(password)
    print(json.dumps({"input": password, "result": asdict(result)}, ensure_ascii=False))
    expected = password == "Ab3!xy7Z"
    assert result.is_valid is expected, (password, result)
print("6 casos comprobados; los 3 exigidos por la guía fueron rechazados.")
