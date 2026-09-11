"""Pruebas de integración en memoria para la CLI."""

import pytest
from temperatura.cli import main


def test_us1_cli_conversion_basica_stdout(capsys):
    ret = main(["100", "C", "F"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "212.00 F"
    assert captured.err == ""


def test_us1_cli_insensible_mayusculas(capsys):
    ret = main(["212", "f", "c"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "100.00 C"


def test_us1_cli_misma_escala(capsys):
    ret = main(["25", "c", "c"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "25.00 C"


def test_us1_cli_negativo_valido(capsys):
    ret = main(["-40", "C", "F"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "-40.00 F"


# --- Pruebas US2: Integración CLI Cero Absoluto ---


def test_us2_cli_rechazo_celsius_bajo_cero_absoluto(capsys):
    ret = main(["-273.16", "C", "F"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "cero absoluto" in captured.err.lower()
    assert captured.out == ""


def test_us2_cli_rechazo_fahrenheit_bajo_cero_absoluto(capsys):
    ret = main(["-459.68", "F", "C"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "cero absoluto" in captured.err.lower()


def test_us2_cli_rechazo_kelvin_negativo(capsys):
    ret = main(["-1", "K", "C"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "cero absoluto" in captured.err.lower()


def test_us2_cli_aceptacion_umbral_exacto(capsys):
    ret = main(["-273.15", "C", "K"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "0.00 K"
    assert captured.err == ""


# --- Pruebas US3: Integración CLI Validaciones y Blindaje ---


def test_us3_cli_argumentos_insuficientes(capsys):
    ret = main(["100", "C"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "exactamente 3 argumentos" in captured.err


def test_us3_cli_argumentos_vacios(capsys):
    ret = main(["", "C", "F"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "no puede estar vacío" in captured.err


def test_us3_cli_no_numerico(capsys):
    ret = main(["abc", "C", "F"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "no es un número válido" in captured.err


@pytest.mark.parametrize("literal", ["nan", "NaN", "NAN", "inf", "Infinity", "-inf", "+inf"])
def test_us3_cli_rechazo_nan_inf(capsys, literal):
    ret = main([literal, "C", "F"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "no están permitidos" in captured.err


def test_us3_cli_longitud_bruta_excesiva_sin_espacios(capsys):
    ret = main(["1" * 33, "C", "F"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "excede el límite permitido de 32 caracteres" in captured.err


def test_us3_cli_longitud_bruta_excesiva_con_relleno_antes_de_strip(capsys):
    # Cadena con espacios cuya longitud ANTES de strip excede 32
    entrada_con_espacios = "   " + ("1" * 30)  # longitud 33
    ret = main([entrada_con_espacios, "C", "F"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "excede el límite permitido de 32 caracteres" in captured.err


def test_us3_cli_longitud_valida_con_espacios_saneados(capsys):
    # Longitud bruta <= 32 pero con espacios alrededor
    ret = main([" 100 ", " c ", " f "])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "212.00 F"


def test_us3_cli_magnitud_excesiva(capsys):
    ret = main(["1e13", "C", "F"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "magnitud máxima permitida" in captured.err


def test_us3_cli_notacion_cientifica_valida(capsys):
    ret = main(["-1e2", "C", "K"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "173.15 K"


def test_us3_cli_unidad_invalida(capsys):
    ret = main(["100", "X", "F"])
    captured = capsys.readouterr()
    assert ret == 2
    assert "Unidad 'X' no válida" in captured.err


# --- Pruebas Fase 6 / Casos de Borde CLI (T030) ---


def test_edge_cli_cero_con_signo_semantica(capsys):
    # -0.001 C C -> 0.00 C
    ret1 = main(["-0.001", "C", "C"])
    cap1 = capsys.readouterr()
    assert ret1 == 0
    assert cap1.out.strip() == "0.00 C"

    # 0 C F -> 32.00 F (no normalizado a cero)
    ret2 = main(["0", "C", "F"])
    cap2 = capsys.readouterr()
    assert ret2 == 0
    assert cap2.out.strip() == "32.00 F"


def test_edge_cli_redondeo_half_up(capsys):
    ret = main(["25.555", "C", "C"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "25.56 C"


def test_edge_cli_corte_exacto_fahrenheit(capsys):
    ret_valido = main(["-459.67", "F", "K"])
    cap_valido = capsys.readouterr()
    assert ret_valido == 0
    assert cap_valido.out.strip() == "0.00 K"

    ret_invalido = main(["-459.671", "F", "K"])
    cap_invalido = capsys.readouterr()
    assert ret_invalido == 2
    assert "cero absoluto" in cap_invalido.err.lower()


# --- Pruebas de Regresión FR-012 y FR-009 (Magnitudes Extremas y Finitud) ---


def test_fr012_cli_magnitud_extrema_overflow(capsys):
    """Verifica que magnitudes extremas como 1e9999999 retornan código 2 con mensaje claro en stderr sin desbordar."""
    ret1 = main(["1e9999999", "C", "F"])
    cap1 = capsys.readouterr()
    assert ret1 == 2
    assert "magnitud máxima permitida" in cap1.err

    ret2 = main(["-1e9999999", "C", "F"])
    cap2 = capsys.readouterr()
    assert ret2 == 2
    assert "magnitud máxima permitida" in cap2.err


def test_fr009_cli_snan_is_finite(capsys):
    """Verifica el rechazo de sNaN activando la verificación de finitud sin excepción no controlada."""
    ret = main(["sNaN", "C", "F"])
    cap = capsys.readouterr()
    assert ret == 2
    assert "no están permitidos" in cap.err or "no es un número válido" in cap.err


# --- Pruebas de Regresión FR-008: Evitar Doble Redondeo en CLI ---


def test_fr008_cli_evitar_doble_redondeo_umbral_inferior(capsys):
    ret = main(["1.0027777777777777777777777777", "C", "F"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "33.80 F"


def test_fr008_cli_umbral_superior(capsys):
    ret = main(["1.0027777777777777777777777778", "C", "F"])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "33.81 F"
