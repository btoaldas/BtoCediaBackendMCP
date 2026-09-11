"""Módulo de dominio para el conversor de temperatura."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP, localcontext
from enum import Enum


class ErrorTemperatura(Exception):
    """Excepción base para errores del dominio de temperatura."""


class ErrorCeroAbsoluto(ErrorTemperatura):
    """Lanzada cuando un valor está por debajo del cero absoluto de la escala."""

    def __init__(self, valor: Decimal, escala: "Escala"):
        self.valor = valor
        self.escala = escala
        super().__init__(
            f"Error: La temperatura {valor:.2f} {escala.value} está por debajo del cero absoluto ({escala.cero_absoluto:.2f} {escala.value})."
        )


class ErrorEntradaInvalida(ErrorTemperatura):
    """Lanzada ante formatos no numéricos, literales no permitidos o unidades inválidas."""


class Escala(Enum):
    """Escalas de temperatura soportadas y sus constantes físicas."""

    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"

    @property
    def cero_absoluto(self) -> Decimal:
        if self == Escala.CELSIUS:
            return Decimal("-273.15")
        elif self == Escala.FAHRENHEIT:
            return Decimal("-459.67")
        elif self == Escala.KELVIN:
            return Decimal("0.0")
        raise NotImplementedError(f"Escala desconocida: {self}")

    @classmethod
    def desde_simbolo(cls, simbolo: str) -> "Escala":
        if not isinstance(simbolo, str):
            raise ErrorEntradaInvalida(f"Error: Unidad '{simbolo}' no válida. Use C, F o K.")
        limpio = simbolo.strip().upper()
        for escala in cls:
            if escala.value == limpio:
                return escala
        raise ErrorEntradaInvalida(f"Error: Unidad '{simbolo}' no válida. Use C, F o K.")


@dataclass(frozen=True)
class LecturaTemperatura:
    """Modela una medición de temperatura con magnitud y escala."""

    valor: Decimal
    escala: Escala

    def __post_init__(self):
        if not self.valor.is_finite():
            raise ErrorEntradaInvalida("Error: Los valores literales 'nan' e 'inf' no están permitidos.")
        if self.valor.copy_abs() > Decimal("1e12"):
            raise ErrorEntradaInvalida(f"Error: El valor '{self.valor}' excede la magnitud máxima permitida (1e12).")
        if self.valor < self.escala.cero_absoluto:
            raise ErrorCeroAbsoluto(self.valor, self.escala)


@dataclass(frozen=True)
class ResultadoConversion:
    """Encapsula el resultado de la conversión entre escalas."""

    valor_original: Decimal
    escala_origen: Escala
    valor_convertido: Decimal
    escala_destino: Escala

    def formatear(self) -> str:
        """Formatea el resultado a dos decimales con redondeo ROUND_HALF_UP usando precisión extendida."""
        with localcontext() as ctx:
            ctx.prec = 80
            cuantizado = self.valor_convertido.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if cuantizado.is_zero():
                cuantizado = Decimal("0.00")
            return f"{cuantizado:.2f} {self.escala_destino.value}"


def convertir(
    valor: Decimal, escala_origen: Escala, escala_destino: Escala
) -> ResultadoConversion:
    """Convierte una temperatura entre dos escalas usando aritmética Decimal de alta precisión local."""
    # Validación termodinámica y de magnitud
    LecturaTemperatura(valor=valor, escala=escala_origen)

    with localcontext() as ctx:
        ctx.prec = 80
        if escala_origen == escala_destino:
            valor_destino = valor
        elif escala_origen == Escala.CELSIUS and escala_destino == Escala.FAHRENHEIT:
            valor_destino = (valor * Decimal("9") / Decimal("5")) + Decimal("32")
        elif escala_origen == Escala.FAHRENHEIT and escala_destino == Escala.CELSIUS:
            valor_destino = (valor - Decimal("32")) * Decimal("5") / Decimal("9")
        elif escala_origen == Escala.CELSIUS and escala_destino == Escala.KELVIN:
            valor_destino = valor + Decimal("273.15")
        elif escala_origen == Escala.KELVIN and escala_destino == Escala.CELSIUS:
            valor_destino = valor - Decimal("273.15")
        elif escala_origen == Escala.FAHRENHEIT and escala_destino == Escala.KELVIN:
            celsius = (valor - Decimal("32")) * Decimal("5") / Decimal("9")
            valor_destino = celsius + Decimal("273.15")
        elif escala_origen == Escala.KELVIN and escala_destino == Escala.FAHRENHEIT:
            celsius = valor - Decimal("273.15")
            valor_destino = (celsius * Decimal("9") / Decimal("5")) + Decimal("32")
        else:
            raise NotImplementedError(f"Conversión no implementada: {escala_origen} -> {escala_destino}")

    return ResultadoConversion(
        valor_original=valor,
        escala_origen=escala_origen,
        valor_convertido=valor_destino,
        escala_destino=escala_destino,
    )
