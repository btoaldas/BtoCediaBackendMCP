# Conversor de Temperatura CLI

Herramienta de línea de comandos para la conversión precisa de temperaturas entre las escalas Celsius (C), Fahrenheit (F) y Kelvin (K) implementada en Python 3.12 con precisión `Decimal` y redondeo `ROUND_HALF_UP`.

## Requisitos

- Python 3.12+
- `uv` (gestor de dependencias y entornos)

## Instalación

Para sincronizar el entorno virtual de forma reproducible utilizando el archivo de bloqueo:

```bash
uv sync --frozen
```

Esto instalará las dependencias necesarias y empaquetará el módulo `temperatura` en modo editable dentro del entorno virtual.

## Uso de la CLI

Invoque el paquete directamente mediante el intérprete del entorno:

```bash
uv run python -m temperatura <valor> <unidad_origen> <unidad_destino>
```

### Ejemplos

```bash
# Conversión estándar de Celsius a Fahrenheit (Ebullición del agua)
uv run python -m temperatura 100 C F
# Salida: 212.00 F

# Cero Celsius a Fahrenheit (preserva el resultado de 32.00 F)
uv run python -m temperatura 0 C F
# Salida: 32.00 F

# Cero absoluto exacto en Celsius a Kelvin
uv run python -m temperatura -273.15 C K
# Salida: 0.00 K

# Rechazo de temperatura por debajo del cero absoluto (código de salida 2)
uv run python -m temperatura -300 C F
# Salida en stderr: Error: La temperatura -300.00 C está por debajo del cero absoluto (-273.15 C).

# Rechazo de literales especiales (código de salida 2)
uv run python -m temperatura NaN C F
# Salida en stderr: Error: Los valores literales 'nan' e 'inf' no están permitidos.
```

## Pruebas

Ejecutar la suite completa de pruebas en tres capas (unitaria, integración en memoria y subprocesos e2e):

```bash
uv run pytest
```
