#!/usr/bin/env python3
"""conversor_agy.py - Conversor de temperatura entre Celsius, Fahrenheit y Kelvin."""

import argparse
import math
import sys

ABSOLUTE_ZERO = {
    "C": -273.15,
    "F": -459.67,
    "K": 0.0,
}


def parse_temperatura(val_str: str) -> float:
    """Parsea y valida que la temperatura sea numérica y finita."""
    if val_str is None or val_str.strip() == "":
        raise argparse.ArgumentTypeError("Entrada vacía o no numérica.")
    try:
        val = float(val_str)
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError(f"Entrada no numérica: '{val_str}'")
    if math.isnan(val) or math.isinf(val):
        raise argparse.ArgumentTypeError(f"Valor no numérico o inválido: '{val_str}'")
    return val


def parse_unidad(unit_str: str) -> str:
    """Parsea y valida las unidades permitidas (C, F, K) sin distinción de mayúsculas."""
    if unit_str is None or unit_str.strip() == "":
        raise argparse.ArgumentTypeError("Unidad vacía o no especificada.")
    u = unit_str.strip().upper()
    if u not in ABSOLUTE_ZERO:
        raise argparse.ArgumentTypeError(
            f"Unidad inválida '{unit_str}'. Acepta únicamente las unidades C, F y K."
        )
    return u


def convertir_temperatura(valor: float, origen: str, destino: str) -> float:
    """
    Convierte una temperatura entre Celsius (C), Fahrenheit (F) y Kelvin (K).
    F↔K se compone a través de las fórmulas C↔F y C↔K.
    """
    origen = origen.upper()
    destino = destino.upper()

    if origen == destino:
        return valor

    # 1. Convertir origen a Celsius
    if origen == "C":
        celsius = valor
    elif origen == "F":
        celsius = (valor - 32.0) * 5.0 / 9.0
    elif origen == "K":
        celsius = valor - 273.15
    else:
        raise ValueError(f"Unidad de origen no válida: {origen}")

    # 2. Convertir Celsius a destino
    if destino == "C":
        resultado = celsius
    elif destino == "F":
        resultado = celsius * 9.0 / 5.0 + 32.0
    elif destino == "K":
        resultado = celsius + 273.15
    else:
        raise ValueError(f"Unidad de destino no válida: {destino}")

    return resultado


def crear_parser() -> argparse.ArgumentParser:
    """Configura y retorna el parser de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="conversor_agy.py",
        description="Convierte temperaturas entre Celsius (C), Fahrenheit (F) y Kelvin (K).",
    )
    parser.add_argument(
        "valor",
        type=parse_temperatura,
        help="Valor numérico de la temperatura a convertir.",
    )
    parser.add_argument(
        "origen",
        type=parse_unidad,
        help="Unidad de origen (C, F, K).",
    )
    parser.add_argument(
        "destino",
        type=parse_unidad,
        help="Unidad de destino (C, F, K).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Punto de entrada de la CLI."""
    parser = crear_parser()

    raw_args = argv if argv is not None else sys.argv[1:]
    if not raw_args:
        parser.error("Entrada vacía: se requieren valor, unidad de origen y unidad de destino.")

    args = parser.parse_args(raw_args)

    limite_cero = ABSOLUTE_ZERO[args.origen]
    if args.valor < limite_cero:
        parser.error(
            f"Temperatura rechazada: {args.valor} {args.origen} está por debajo del cero absoluto "
            f"({limite_cero} {args.origen})."
        )

    resultado = convertir_temperatura(args.valor, args.origen, args.destino)

    # Prevenir representación de -0.00 tras redondeo
    if round(resultado, 2) == 0.0:
        resultado = 0.0

    print(f"{resultado:.2f} {args.destino}")


if __name__ == "__main__":
    main()
