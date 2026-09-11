from dataclasses import asdict
from datetime import datetime, timezone
import json
from evidencia_util import cargar

anterior = cargar("01-contrasenas")
actual = cargar("02-email")
print("RONDA 2 — predicción previa en evidencia/p02/prediccion-02.json")
print("EJECUCIÓN UTC:", datetime.now(timezone.utc).isoformat())
for email, expected in [("ana@correo.com", True), ("ana@", False), ("", False)]:
    result = actual.validate_email(email)
    print(json.dumps({"email": email, "result": asdict(result)}, ensure_ascii=False))
    assert result.is_valid is expected
    assert result.strength is None
for password in ["12345", "password", "", "Ab3!xy7", "Ab3!xy7Z", "Password1!"]:
    before = asdict(anterior.validate_password(password))
    after = asdict(actual.validate_password(password))
    assert before == after, (password, before, after)
    print(json.dumps({"regresion_contrasena": password, "sin_cambios": before == after}, ensure_ascii=False))
print("3 emails comprobados y 6 regresiones de contraseña sin diferencias.")
