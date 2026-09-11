from dataclasses import asdict
from datetime import datetime, timezone
import json
from evidencia_util import cargar

anterior = cargar("03-usuarios")
actual = cargar("04-administradores")
print("CIERRE — predicción previa en evidencia/p02/prediccion-04.json")
print("PEDIDO: ahora que la validación de contraseña sea opcional para usuarios administradores")
print("EJECUCIÓN UTC:", datetime.now(timezone.utc).isoformat())
casos = [
    ("regular_vacio", False, "", "uno@example.com", None, False),
    ("admin_vacio", True, "", "dos@example.com", None, True),
    ("admin_email_invalido", True, "", "ana@", None, False),
    ("admin_forzar_validacion", True, "12345", "tres@example.com", True, False),
    ("booleano_false", False, "12345", "cuatro@example.com", None, False),
    ("cadena_false", "false", "12345", "cinco@example.com", None, True),
    ("cadena_usuario", "usuario", "12345", "seis@example.com", None, True),
]
for name, flag, password, email, enforce, observed in casos:
    user = actual.User(name, email, password, is_admin=flag)
    result = actual.validate_user(user, validate_admin_password=enforce)
    print(json.dumps({"caso": name, "is_admin": flag, "tipo_is_admin": type(flag).__name__,
                      "valido": result.is_valid, "email_valido": result.email_result.is_valid,
                      "password": asdict(result.password_result)}, ensure_ascii=False))
    assert result.is_valid is observed
for value in ["12345", "password", "", "Ab3!xy7", "Ab3!xy7Z", "Password1!"]:
    assert asdict(anterior.validate_password(value)) == asdict(actual.validate_password(value))
for value in ["ana@correo.com", "ana@", ""]:
    assert asdict(anterior.validate_email(value)) == asdict(actual.validate_email(value))
print("REGRESIÓN: 9 respuestas de funciones previas conservadas.")
print("FALLA OBSERVADA: is_admin='false' (str) y 'usuario' (str) activan la exención.")
print("CAUSA: if user.is_admin usa truthiness; dataclass no impone el tipo bool en ejecución.")
print("La hipótesis de saltarse el email NO ocurrió: ana@ sigue rechazado para admin.")
