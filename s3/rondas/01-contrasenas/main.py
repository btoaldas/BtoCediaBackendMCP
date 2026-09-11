from dataclasses import dataclass, field
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
  """Resultado de la validación."""

  is_valid: bool
  errors: list[str]
  strength: str  # 'Débil', 'Media', 'Fuerte'


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

  # Caracteres únicos (penaliza repeticiones continuas como 'aaaaaa1!A')
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


if __name__ == "__main__":
  # Ejemplos de prueba rápidos
  test_passwords = [
      "pass",  # Muy corta
      "password123!",  # Patrón prohibido
      "Temporal2024",  # Sin especial
      "Temp2024!",  # Válida (Media)
      "K9#mQ!9vLp@4WxZ",  # Fuerte
  ]

  print("=== Pruebas del Validador ===")
  for pwd in test_passwords:
    res = validate_password(pwd)
    status = "✓ VÁLIDA" if res.is_valid else "✗ INVÁLIDA"
    print(f"\nContraseña: '{pwd}'")
    print(f"Estado:     {status} ({res.strength})")
    if res.errors:
      for err in res.errors:
        print(f" - {err}")
