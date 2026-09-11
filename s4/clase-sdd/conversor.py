"""Conversor construido a partir de la spec manual; entrada y salida CLI."""
import argparse
from decimal import Decimal, InvalidOperation, localcontext


def convertir(valor: str, origen: str, destino: str) -> Decimal:
    origen, destino = origen.upper(), destino.upper()
    if origen not in ("C", "F", "K") or destino not in ("C", "F", "K"):
        raise ValueError("Las unidades deben ser C, F o K.")
    if len(valor) > 100:
        raise ValueError("La entrada supera 100 caracteres.")
    try:
        numero = Decimal(valor)
    except InvalidOperation as exc:
        raise ValueError("La temperatura debe ser un número.") from exc
    if not numero.is_finite() or abs(numero) > Decimal("1e20"):
        raise ValueError("La temperatura debe ser finita y su magnitud no superar 1e20.")
    if numero < {"C": Decimal("-273.15"), "F": Decimal("-459.67"), "K": Decimal("0")}[origen]:
        raise ValueError("La temperatura está por debajo del cero absoluto.")
    with localcontext() as context:
        context.prec = 40
        celsius = numero if origen == "C" else (numero - 32) * 5 / 9 if origen == "F" else numero - Decimal("273.15")
        return celsius if destino == "C" else celsius * 9 / 5 + 32 if destino == "F" else celsius + Decimal("273.15")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Conversor de temperatura")
    parser.add_argument("valor")
    parser.add_argument("origen")
    parser.add_argument("destino")
    args = parser.parse_args(argv)
    try:
        resultado = convertir(args.valor, args.origen, args.destino)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"{resultado:.2f} {args.destino.upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
