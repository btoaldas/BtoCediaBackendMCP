# Quickstart Guide: Conversor de Temperatura CLI

**Feature**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)
**Contrato CLI**: [cli-contract.md](contracts/cli-contract.md)
**Date**: 2026-09-10

Guía rápida y ejecutable para validar de extremo a extremo la funcionalidad, suites de pruebas y casos de borde del conversor de temperatura.

---

## 1. Requisitos Previos

- Python 3.12+
- `uv` (gestor de entornos y paquetes de Python)

---

## 2. Configuración Inicial del Entorno

Desde la raíz del proyecto (`.`):

```bash
# Sincronizar o verificar el entorno virtual local con uv
uv venv
```

---

## 3. Escenarios de Validación Rápida (CLI)

### 3.1 Conversiones Exitosas (Código de Salida 0)

1. **Conversión Celsius a Fahrenheit (Ebullición del agua)**:
   ```bash
   uv run python -m temperatura 100 C F
   # Salida esperada (stdout): 212.00 F
   # Código de salida: 0
   ```

2. **Conversión Fahrenheit a Celsius (Congelación del agua)**:
   ```bash
   uv run python -m temperatura 32 f c
   # Salida esperada (stdout): 0.00 C
   # Código de salida: 0
   ```

3. **Conversión Celsius a Kelvin (Cero absoluto exacto)**:
   ```bash
   uv run python -m temperatura -273.15 C K
   # Salida esperada (stdout): 0.00 K
   # Código de salida: 0
   ```

4. **Preservación de Misma Unidad**:
   ```bash
   uv run python -m temperatura 25.5 C C
   # Salida esperada (stdout): 25.50 C
   # Código de salida: 0
   ```

5. **Notación Científica Válida**:
   ```bash
   uv run python -m temperatura -1e2 C K
   # Salida esperada (stdout): 173.15 K
   # Código de salida: 0
   ```

---

### 3.2 Escenarios de Rechazo y Error (Código de Salida 2)

1. **Temperatura bajo el cero absoluto**:
   ```bash
   uv run python -m temperatura -300 C F
   # Salida esperada (stderr): Error: La temperatura -300.00 C está por debajo del cero absoluto (-273.15 C).
   # Código de salida: 2
   ```

2. **Rechazo de literal NaN / Infinito**:
   ```bash
   uv run python -m temperatura nan C F
   # Salida esperada (stderr): Error: Los valores literales 'nan' e 'inf' no están permitidos.
   # Código de salida: 2
   ```

3. **Rechazo por longitud superior a 32 caracteres**:
   ```bash
   uv run python -m temperatura 123456789012345678901234567890123 C F
   # Salida esperada (stderr): Error: La longitud del valor numérico excede el límite permitido de 32 caracteres.
   # Código de salida: 2
   ```

4. **Entrada no numérica**:
   ```bash
   uv run python -m temperatura abc C F
   # Salida esperada (stderr): Error: El valor 'abc' no es un número válido.
   # Código de salida: 2
   ```

5. **Unidad no soportada**:
   ```bash
   uv run python -m temperatura 100 X F
   # Salida esperada (stderr): Error: Unidad 'X' no válida. Use C, F o K.
   # Código de salida: 2
   ```

---

## 4. Ejecución de la Batería de Pruebas (3 Capas)

La suite se compone de tres niveles de verificación complementarios:

```bash
# Capa 1: Pruebas unitarias de dominio matemático y validación aislada
uv run pytest tests/unit

# Capa 2: Pruebas de integración CLI en memoria (captura de capsys, sin subprocess)
uv run pytest tests/integration

# Capa 3: Pruebas End-to-End invocando el proceso completo con subproceso del sistema operativo
uv run pytest tests/e2e

# Ejecutar la suite completa con informe de cobertura
uv run pytest --cov=src/temperatura tests/
```
