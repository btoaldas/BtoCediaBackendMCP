"""Pruebas unitarias de dominio para el conversor de temperatura."""

from decimal import Decimal
import pytest

from temperatura.dominio import (
    Escala,
    LecturaTemperatura,
    ResultadoConversion,
    convertir,
)


def test_us1_conversion_celsius_a_fahrenheit():
    resultado = convertir(Decimal("100"), Escala.CELSIUS, Escala.FAHRENHEIT)
    assert resultado.formatear() == "212.00 F"


def test_us1_conversion_fahrenheit_a_celsius():
    resultado = convertir(Decimal("212"), Escala.FAHRENHEIT, Escala.CELSIUS)
    assert resultado.formatear() == "100.00 C"


def test_us1_conversion_celsius_a_kelvin():
    resultado = convertir(Decimal("0"), Escala.CELSIUS, Escala.KELVIN)
    assert resultado.formatear() == "273.15 K"


def test_us1_conversion_kelvin_a_celsius():
    resultado = convertir(Decimal("373.15"), Escala.KELVIN, Escala.CELSIUS)
    assert resultado.formatear() == "100.00 C"


def test_us1_conversion_fahrenheit_a_kelvin():
    resultado = convertir(Decimal("32"), Escala.FAHRENHEIT, Escala.KELVIN)
    assert resultado.formatear() == "273.15 K"


def test_us1_conversion_kelvin_a_fahrenheit():
    resultado = convertir(Decimal("273.15"), Escala.KELVIN, Escala.FAHRENHEIT)
    assert resultado.formatear() == "32.00 F"


def test_us1_preservacion_misma_escala():
    resultado = convertir(Decimal("25"), Escala.CELSIUS, Escala.CELSIUS)
    assert resultado.formatear() == "25.00 C"


def test_us1_negativo_valido_coincidencia():
    resultado = convertir(Decimal("-40"), Escala.CELSIUS, Escala.FAHRENHEIT)
    assert resultado.formatear() == "-40.00 F"


# --- Pruebas US2: Cero Absoluto ---

from temperatura.dominio import ErrorCeroAbsoluto


def test_us2_rechazo_celsius_bajo_cero_absoluto():
    with pytest.raises(ErrorCeroAbsoluto):
        convertir(Decimal("-273.16"), Escala.CELSIUS, Escala.FAHRENHEIT)


def test_us2_rechazo_fahrenheit_bajo_cero_absoluto():
    with pytest.raises(ErrorCeroAbsoluto):
        convertir(Decimal("-459.68"), Escala.FAHRENHEIT, Escala.CELSIUS)


def test_us2_rechazo_kelvin_negativo():
    with pytest.raises(ErrorCeroAbsoluto):
        convertir(Decimal("-0.01"), Escala.KELVIN, Escala.CELSIUS)


def test_us2_aceptacion_umbral_exacto_celsius():
    resultado = convertir(Decimal("-273.15"), Escala.CELSIUS, Escala.KELVIN)
    assert resultado.formatear() == "0.00 K"


def test_us2_aceptacion_umbral_exacto_fahrenheit():
    resultado = convertir(Decimal("-459.67"), Escala.FAHRENHEIT, Escala.CELSIUS)
    assert resultado.formatear() == "-273.15 C"


def test_us2_aceptacion_umbral_exacto_kelvin():
    resultado = convertir(Decimal("0"), Escala.KELVIN, Escala.CELSIUS)
    assert resultado.formatear() == "-273.15 C"


# --- Pruebas US3: Validaciones de Entrada en Dominio ---

from temperatura.dominio import ErrorEntradaInvalida


def test_us3_dominio_unidad_invalida():
    with pytest.raises(ErrorEntradaInvalida):
        Escala.desde_simbolo("X")


def test_us3_dominio_unidad_tipo_no_str():
    with pytest.raises(ErrorEntradaInvalida):
        Escala.desde_simbolo(123)  # type: ignore


# --- Pruebas Fase 6 / Casos de Borde (T030) ---


def test_edge_normalizacion_cero_con_signo_solo_cuando_resultado_es_cero():
    # Caso 1: Resultado que redondea a cero negativo debe mostrar 0.00
    res_cero = convertir(Decimal("-0.0001"), Escala.CELSIUS, Escala.CELSIUS)
    assert res_cero.formatear() == "0.00 C"

    # Caso 2: 0 C a F debe ser 32.00 F, ¡NO 0.00 F!
    res_no_cero = convertir(Decimal("0"), Escala.CELSIUS, Escala.FAHRENHEIT)
    assert res_no_cero.formatear() == "32.00 F"


def test_edge_redondeo_round_half_up():
    res = convertir(Decimal("25.555"), Escala.CELSIUS, Escala.CELSIUS)
    assert res.formatear() == "25.56 C"


def test_edge_corte_exacto_fahrenheit_cero_absoluto():
    # Exacto: -459.67 F permitido
    res_valido = convertir(Decimal("-459.67"), Escala.FAHRENHEIT, Escala.CELSIUS)
    assert res_valido.formatear() == "-273.15 C"

    # Inferior por un milésimo: -459.671 F rechazado
    with pytest.raises(ErrorCeroAbsoluto):
        convertir(Decimal("-459.671"), Escala.FAHRENHEIT, Escala.CELSIUS)
