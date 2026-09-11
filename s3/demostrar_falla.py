"""Segunda reproducción: este programa DEBE terminar con AssertionError.

Es la falla conservada del experimento sin spec, no una prueba de éxito.
"""
from datetime import datetime, timezone
import json
from evidencia_util import cargar

module = cargar("04-administradores")
payload = '{"username":"usuario_entrada","email":"entrada@example.com","password":"12345","is_admin":"false"}'
user = module.User(**json.loads(payload))
result = module.validate_users([user])[0]
print("SEGUNDA REPRODUCCIÓN DE LA FALLA — entrada JSON sintética", flush=True)
print("EJECUCIÓN UTC:", datetime.now(timezone.utc).isoformat(), flush=True)
print(payload, flush=True)
print("tipo is_admin:", type(user.is_admin).__name__, flush=True)
print("validez contraseña directa:", module.validate_password(user.password).is_valid, flush=True)
print("validez usuario en lote:", result.is_valid, flush=True)
assert not result.is_valid, "FALLA: el texto 'false' activa la exención de administrador"
