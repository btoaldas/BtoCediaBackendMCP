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
  """Resultado general de validación."""

  is_valid: bool
  errors: list[str]
  strength: str | None = None  # 'Débil', 'Media', 'Fuerte' (solo contraseñas)


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


def validate_email(email: str) -> ValidationResult:
  """Valida el formato de una dirección de correo electrónico según RFC 5321/5322."""
  errors: list[str] = []

  if not email:
    return ValidationResult(
        is_valid=False, errors=["La dirección de correo no puede estar vacía."]
    )

  # 1. Espacios en blanco
  if any(c.isspace() for c in email):
    errors.append("No se permiten espacios en blanco.")

  # 2. Longitud total máxima (RFC 5321)
  if len(email) > 254:
    errors.append(
        f"No puede exceder los 254 caracteres (actual: {len(email)})."
    )

  # 3. Estructura de arroba
  if "@" not in email:
    errors.append("Falta el carácter '@'.")
    return ValidationResult(is_valid=False, errors=errors)

  if email.count("@") > 1:
    errors.append("Debe contener exactamente un carácter '@'.")
    return ValidationResult(is_valid=False, errors=errors)

  local_part, domain_part = email.split("@")

  # 4. Validación de la parte local (usuario)
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

  # 5. Validación de dominio
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
              f"La etiqueta de dominio '{label}' contiene caracteres no"
              " válidos."
          )

      tld = labels[-1]
      if not tld.isalpha() or len(tld) < 2:
        errors.append(
            f"El dominio superior (TLD) '{tld}' debe ser alfabético y tener al"
            " menos 2 caracteres."
        )

  is_valid = len(errors) == 0
  return ValidationResult(is_valid=is_valid, errors=errors)


if __name__ == "__main__":
  # Pruebas de Contraseñas
  test_passwords = [
      "pass",  # Muy corta
      "password123!",  # Patrón prohibido
      "Temporal2024",  # Sin especial
      "Temp2024!",  # Válida (Media)
      "K9#mQ!9vLp@4WxZ",  # Fuerte
  ]

  print("=== Pruebas de Contraseñas ===")
  for pwd in test_passwords:
    res = validate_password(pwd)
    status = "✓ VÁLIDA" if res.is_valid else "✗ INVÁLIDA"
    print(f"\nContraseña: '{pwd}'")
    print(f"Estado:     {status} ({res.strength})")
    if res.errors:
      for err in res.errors:
        print(f" - {err}")

  # Pruebas de Correos
  test_emails = [
      "usuario@dominio.com",  # Válido simple
      "nombre.apellido+tag@empresa.co.uk",  # Válido con subdominios y tags
      "sin_arroba.com",  # Falta arroba
      "usuario@dominio",  # Falta TLD
      "usuario..doblepunto@dominio.com",  # Puntos consecutivos
      "@sindominio.com",  # Sin parte local
      "usuario@dominio..com",  # Puntos consecutivos en dominio
      "usuario@-dominio.com",  # Guion al inicio de etiqueta
      "usuario@dominio.123",  # TLD numérico
  ]

  print("\n=== Pruebas de Correo Electrónico ===")
  for email in test_emails:
    res = validate_email(email)
    status = "✓ VÁLIDO" if res.is_valid else "✗ INVÁLIDO"
    print(f"\nCorreo: '{email}'")
    print(f"Estado: {status}")
    if res.errors:
      for err in res.errors:
        print(f" - {err}")
