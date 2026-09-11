"""Módulo de interfaz de línea de comandos para el conversor de temperatura."""

from decimal import Decimal, InvalidOperation
import sys

from temperatura.dominio import Escala, convertir, ErrorTemperatura


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada para la CLI."""
    if argv is None:
        argv = sys.argv[1:]

    # 1. Validación de número de argumentos
    if len(argv) != 3:
        sys.stderr.write("Error: Se requieren exactamente 3 argumentos: <valor> <unidad_origen> <unidad_destino>\n")
        return 2

    raw_valor, raw_origen, raw_destino = argv

    # 2. Validación de longitud de cadena ANTES de strip
    if len(raw_valor) > 32:
        sys.stderr.write("Error: La longitud del valor numérico excede el límite permitido de 32 caracteres.\n")
        return 2

    # 3. Saneamiento de espacios
    valor_limpio = raw_valor.strip()
    if not valor_limpio:
        sys.stderr.write("Error: El valor no puede estar vacío.\n")
        return 2

    # 4. Filtrado estricto de literales no permitidos (NaN / Inf)
    literal_check = valor_limpio.lower()
    if literal_check in ("nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"):
        sys.stderr.write("Error: Los valores literales 'nan' e 'inf' no están permitidos.\n")
        return 2

    # 5. Conversión a Decimal y verificación de número válido
    try:
        valor = Decimal(valor_limpio)
    except (InvalidOperation, Exception):
        sys.stderr.write(f"Error: El valor '{valor_limpio}' no es un número válido.\n")
        return 2

    # 6. Finitud y magnitud
    if not valor.is_finite():
        sys.stderr.write("Error: Los valores literales 'nan' e 'inf' no están permitidos.\n")
        return 2

    if abs(valor) > Decimal("1e12"):
        sys.stderr.write(f"Error: El valor '{valor_limpio}' excede la magnitud máxima permitida (1e12).\n")
        return 2

    # 7. Conversión y ejecución en dominio
    try:
        escala_origen = Escala.desde_simbolo(raw_origen)
        escala_destino = Escala.desde_simbolo(raw_destino)
        resultado = convertir(valor, escala_origen, escala_destino)
        sys.stdout.write(f"{resultado.formatear()}\n")
        return 0
    except ErrorTemperatura as err:
        sys.stderr.write(f"{err}\n")
        return 2
    except Exception as err:
        sys.stderr.write(f"Error: {err}\n")
        return 2
