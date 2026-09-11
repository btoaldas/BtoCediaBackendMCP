from dataclasses import asdict
from datetime import datetime, timezone
import json
from evidencia_util import cargar

anterior = cargar("02-email")
actual = cargar("03-usuarios")
print("RONDA 3 — predicción previa en evidencia/p02/prediccion-03.json")
print("EJECUCIÓN UTC:", datetime.now(timezone.utc).isoformat())
usuarios = []
usuarios.append(actual.User("usuario_1", "ana@example.com", "Ab3!xy7Z"))
usuarios.append(actual.User("usuario_2", "bruno@example.com", "K9#mQ!9vLp@4WxZ"))
print("DOS USUARIOS AGREGADOS; LISTA COMPLETA (datos sintéticos):")
print(json.dumps([asdict(user) for user in usuarios], ensure_ascii=False))
resultados = actual.validate_users(usuarios)
for result in resultados:
    print(json.dumps({"usuario": result.user.username, "valido": result.is_valid,
                      "email": asdict(result.email_result),
                      "password": asdict(result.password_result),
                      "errores_extra": result.extra_errors}, ensure_ascii=False))
assert len(resultados) == 2 and all(result.is_valid for result in resultados)
for value in ["12345", "password", "", "Ab3!xy7", "Ab3!xy7Z", "Password1!"]:
    assert asdict(anterior.validate_password(value)) == asdict(actual.validate_password(value))
for value in ["ana@correo.com", "ana@", ""]:
    assert asdict(anterior.validate_email(value)) == asdict(actual.validate_email(value))
print("REGRESIÓN: 6 contraseñas + 3 emails conservan resultado.")
duplicados = actual.validate_users([
    actual.User("uno", "dup@example.com", "Ab3!xy7Z"),
    actual.User("dos", "dup@example.com", "Ab3!xy7Z"),
])
assert all(not r.is_valid and r.extra_errors for r in duplicados)
print("REGLA NO PEDIDA: email duplicado invalida ambos usuarios:", duplicados[0].extra_errors)
vacio = actual.validate_user(actual.User("", "ana@example.com", "Ab3!xy7Z"))
assert not vacio.is_valid and vacio.extra_errors
print("REGLA NO PEDIDA: username vacío rechazado:", vacio.extra_errors)
print("Prueba terminada: lista en memoria con dataclass User y resultados por campo.")
