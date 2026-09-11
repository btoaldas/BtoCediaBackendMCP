Aquí tienes el código Python completo y listo para producción, integrando la abstracción para modelar usuarios (`User`), validar sus credenciales individuales (`validate_user`) y procesar lotes completos de usuarios (`validate_users`) con un reporte estructurado.

```python
from dataclasses import dataclass, field
import re
import sys


@dataclass
class PasswordPolicy:
  """Configuración de reglas de validación para contraseñas."""

  min_length: int = 8
  max_length: int = 128
  require_uppercase: bool = True
  require_lowercase: bool = True
  require_digit: bool = True
  require_special: bool = True
  disallow_whitespace: bool = True
  special_chars: str = r"!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
  forbidden_substrings: list[str] = field(
      default_factory=lambda: [
          "123456",
          "password",
          "contrasena",
          "admin",
          "qwerty",
          "111111",
      ]
  )


@dataclass
class ValidationResult:
  """Resultado general de validación para un campo específico."""

  is_valid: bool
  errors: list[str]
  strength: str | None = None  # 'Débil', 'Media', 'Fuerte' (solo contraseñas)


@dataclass
class User:
  """Representa a un usuario con sus credenciales básicas."""

  username: str
  email: str
  password: str


@dataclass
class UserValidationResult:
  """Resultado consolidado de la validación de un usuario."""

  user: User
  email_result: ValidationResult
  password_result: ValidationResult
  extra_errors: list[str] = field(default_factory=list)

  @property
  def is_valid(self) -> bool:
    return (
        self.email_result.is_valid
        and self.password_result.is_valid
        and len(self.extra_errors) == 0
    )


def validate_password(
    password: str, policy: PasswordPolicy | None = None
) -> ValidationResult:
  """Valida una contraseña contra una política y calcula su robustez."""
  if policy is None:
    policy = PasswordPolicy()

  errors: list[str] = []

  # 1. Reglas de longitud
  if len(password) < policy.min_length:
    errors.append(
        f"Debe tener al menos {policy.min_length} caracteres (actual:"
        f" {len(password)})."
    )
  if len(password) > policy.max_length:
    errors.append(
        f"No puede exceder {policy.max_length} caracteres (actual:"
        f" {len(password)})."
    )

  # 2. Espacios en blanco
  if policy.disallow_whitespace and any(c.isspace() for c in password):
    errors.append("No se permiten espacios en blanco.")

  # 3. Composición de caracteres
  has_upper = any(c.isupper() for c in password)
  has_lower = any(c.islower() for c in password)
  has_digit = any(c.isdigit() for c in password)
  has_special = any(c in policy.special_chars for c in password)

  if policy.require_uppercase and not has_upper:
    errors.append("Debe contener al menos una letra mayúscula.")
  if policy.require_lowercase and not has_lower:
    errors.append("Debe contener al menos una letra minúscula.")
  if policy.require_digit and not has_digit:
    errors.append("Debe contener al menos un número.")
  if policy.require_special and not has_special:
    errors.append("Debe contener al menos un carácter especial.")

  # 4. Palabras comunes o secuencias triviales
  lower_password = password.lower()
  for pattern in policy.forbidden_substrings:
    if pattern in lower_password:
      errors.append(f"Contiene un patrón trivial o inseguro: '{pattern}'.")

  is_valid = len(errors) == 0

  # 5. Estimación de fortaleza
  score = 0
  if len(password) >= 12:
    score += 2
  elif len(password) >= 8:
    score += 1

  if has_upper:
    score += 1
  if has_lower:
    score += 1
  if has_digit:
    score += 1
  if has_special:
    score += 1

  unique_ratio = len(set(password)) / len(password) if password else 0
  if unique_ratio > 0.7:
    score += 1

  if is_valid and score >= 6:
    strength = "Fuerte"
  elif is_valid or score >= 4:
    strength = "Media"
  else:
    strength = "Débil"

  return ValidationResult(is_valid=is_valid, errors=errors, strength=strength)


def validate_email(email: str) -> ValidationResult:
  """Valida el formato de una dirección de correo electrónico según RFC 5321/5322."""
  errors: list[str] = []

  if not email:
    return ValidationResult(
        is_valid=False, errors=["La dirección de correo no puede estar vacía."]
    )

  if any(c.isspace() for c in email):
    errors.append("No se permiten espacios en blanco.")

  if len(email) > 254:
    errors.append(
        f"No puede exceder los 254 caracteres (actual: {len(email)})."
    )

  if "@" not in email:
    errors.append("Falta el carácter '@'.")
    return ValidationResult(is_valid=False, errors=errors)

  if email.count("@") > 1:
    errors.append("Debe contener exactamente un carácter '@'.")
    return ValidationResult(is_valid=False, errors=errors)

  local_part, domain_part = email.split("@")

  if not local_part:
    errors.append("La parte local (antes del '@') no puede estar vacía.")
  elif len(local_part) > 64:
    errors.append(
        "La parte local no puede exceder 64 caracteres (actual:"
        f" {len(local_part)})."
    )
  elif local_part.startswith(".") or local_part.endswith("."):
    errors.append("La parte local no puede empezar ni terminar con un punto.")
  elif ".." in local_part:
    errors.append("La parte local no puede contener puntos consecutivos.")
  elif not re.fullmatch(r"[a-zA-Z0-9!#$%&'*+/=?^_`{|}~.-]+", local_part):
    errors.append("La parte local contiene caracteres no permitidos.")

  if not domain_part:
    errors.append("El dominio (después del '@') no puede estar vacío.")
  elif len(domain_part) > 253:
    errors.append(
        f"El dominio no puede exceder 253 caracteres (actual: {len(domain_part)})."
    )
  elif domain_part.startswith(".") or domain_part.endswith("."):
    errors.append("El dominio no puede empezar ni terminar con un punto.")
  elif ".." in domain_part:
    errors.append("El dominio no puede contener puntos consecutivos.")
  else:
    labels = domain_part.split(".")
    if len(labels) < 2:
      errors.append(
          "El dominio debe contener al menos un punto separando el nombre y la"
          " extensión (ej. .com)."
      )
    else:
      for label in labels:
        if not label:
          errors.append("El dominio contiene una etiqueta vacía.")
        elif len(label) > 63:
          errors.append(
              f"La etiqueta de dominio '{label}' supera los 63 caracteres."
          )
        elif label.startswith("-") or label.endswith("-"):
          errors.append(
              f"La etiqueta de dominio '{label}' no puede iniciar ni terminar"
              " con guion."
          )
        elif not re.fullmatch(r"[a-zA-Z0-9-]+", label):
          errors.append(
              f"La etiqueta de dominio '{label}' contiene caracteres no válidos."
          )

      tld = labels[-1]
      if not tld.isalpha() or len(tld) < 2:
        errors.append(
            f"El dominio superior (TLD) '{tld}' debe ser alfabético y tener al"
            " menos 2 caracteres."
        )

  is_valid = len(errors) == 0
  return ValidationResult(is_valid=is_valid, errors=errors)


def validate_user(
    user: User, policy: PasswordPolicy | None = None
) -> UserValidationResult:
  """Valida las credenciales individuales de un usuario."""
  extra_errors: list[str] = []
  if not user.username or not user.username.strip():
    extra_errors.append("El nombre de usuario no puede estar vacío.")

  email_res = validate_email(user.email)
  pwd_res = validate_password(user.password, policy)

  return UserValidationResult(
      user=user,
      email_result=email_res,
      password_result=pwd_res,
      extra_errors=extra_errors,
  )


def validate_users(
    users: list[User],
    policy: PasswordPolicy | None = None,
    check_duplicates: bool = True,
) -> list[UserValidationResult]:
  """Valida una lista de usuarios y detecta correos duplicados en el lote."""
  results: list[UserValidationResult] = []
  seen_emails: dict[str, int] = {}

  for user in users:
    res = validate_user(user, policy)
    results.append(res)
    normalized_email = user.email.strip().lower()
    if normalized_email:
      seen_emails[normalized_email] = seen_emails.get(normalized_email, 0) + 1

  if check_duplicates:
    for res in results:
      normalized_email = res.user.email.strip().lower()
      if seen_emails.get(normalized_email, 0) > 1:
        res.extra_errors.append(
            f"El correo '{res.user.email}' está duplicado en el lote."
        )

  return results


if __name__ == "__main__":
  # Lista de usuarios de prueba cubriendo distintos escenarios
  users_batch = [
      User(
          username="alberto_adm",
          email="alberto@empresa.com",
          password="K9#mQ!9vLp@4WxZ",  # Válido (Fuerte)
      ),
      User(
          username="maria_dev",
          email="maria.gonzalez@dominio.org",
          password="Temp2024!",  # Válido (Media)
      ),
      User(
          username="carlos_qa",
          email="carlos..invalido@dominio.com",  # Email inválido (puntos dobles)
          password="Password123!",  # Contraseña inválida (patrón prohibido)
      ),
      User(
          username="lucia_ops",
          email="lucia@sub.empresa.co.uk",  # Email válido
          password="corta",  # Contraseña inválida (muy corta, sin requerimientos)
      ),
      User(
          username="usuario_duplicado",
          email="alberto@empresa.com",  # Email duplicado respecto al primer usuario
          password="Segura_2024#Ok",
      ),
      User(
          username="",  # Nombre de usuario vacío
          email="sin_arroba.net",  # Email inválido
          password="Valida123!Password",  # Contraseña contiene 'password'
      ),
  ]

  print("=== Procesando Validación de Lista de Usuarios ===\n")
  validation_results = validate_users(users_batch)

  valid_count = 0
  invalid_count = 0

  for idx, res in enumerate(validation_results, start=1):
    u = res.user
    if res.is_valid:
      valid_count += 1
      status_label = "✓ VÁLIDO"
    else:
      invalid_count += 1
      status_label = "✗ INVÁLIDO"

    print(f"[{idx}] Usuario: '{u.username}' | Estado General: {status_label}")
    print(f"    - Email:    '{u.email}' -> {'✓ OK' if res.email_result.is_valid else '✗ ERROR'}")
    if res.email_result.errors:
      for err in res.email_result.errors:
        print(f"        * {err}")

    print(
        f"    - Password: [Robustez: {res.password_result.strength}] -> "
        f"{'✓ OK' if res.password_result.is_valid else '✗ ERROR'}"
    )
    if res.password_result.errors:
      for err in res.password_result.errors:
        print(f"        * {err}")

    if res.extra_errors:
      for err in res.extra_errors:
        print(f"    - Alerta de lote/cuenta: {err}")

    print("-" * 65)

  print("\n=== Resumen de Ejecución ===")
  print(f"Total procesados: {len(validation_results)}")
  print(f"Usuarios válidos:   {valid_count}")
  print(f"Usuarios inválidos: {invalid_count}")
```

### Cambios principales introducidos:
1. **Modelado con `User`**: Estructura tipada mediante `@dataclass` que encapsula `username`, `email` y `password`.
2. **Resultado unificado (`UserValidationResult`)**: Consolida la evaluación del correo, la contraseña y las reglas globales de cuenta mediante la propiedad booleana `is_valid`.
3. **Validación en lote (`validate_users`)**: Itera la lista completa de usuarios, valida cada elemento y añade detección de correos duplicados en el lote.
4. **Informe de consola**: Formato de salida que detalla el estado individual por campo, la fortaleza de cada contraseña y un balance consolidado al final.
