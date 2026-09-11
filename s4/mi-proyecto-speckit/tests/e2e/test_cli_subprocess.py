"""Pruebas end-to-end con subproceso para la CLI."""

import subprocess
import sys


def test_us1_e2e_conversion_proceso_real():
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "100", "C", "F"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "212.00 F"
    assert result.stderr == ""


def test_us1_e2e_conversion_kelvin_proceso_real():
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "0", "c", "k"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "273.15 K"


# --- Pruebas US2: E2E Cero Absoluto ---


def test_us2_e2e_rechazo_bajo_cero_absoluto():
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "-300", "C", "F"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "cero absoluto" in result.stderr.lower()
    assert result.stdout == ""


def test_us2_e2e_aceptacion_umbral_exacto():
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "0", "K", "C"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "-273.15 C"


# --- Pruebas US3: E2E Validaciones y Blindaje ---


def test_us3_e2e_rechazo_nan():
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "nan", "C", "F"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "no están permitidos" in result.stderr
    assert result.stdout == ""


def test_us3_e2e_notacion_cientifica():
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "-1e2", "C", "K"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "173.15 K"


def test_us3_e2e_longitud_bruta_excede_32():
    entrada_larga = " " * 10 + "100" + " " * 20  # 33 caracteres
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", entrada_larga, "C", "F"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "excede el límite permitido de 32 caracteres" in result.stderr


def test_us3_e2e_unidad_invalida():
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "100", "X", "F"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "no válida" in result.stderr


# --- Pruebas de Regresión FR-012 E2E ---


def test_fr012_e2e_magnitud_extrema_overflow():
    """Verifica en subproceso real que 1e9999999 concluye con returncode 2 sin Traceback."""
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "1e9999999", "C", "F"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert "magnitud máxima permitida" in result.stderr


# --- Pruebas de Regresión FR-008 E2E: Doble Redondeo ---


def test_fr008_e2e_evitar_doble_redondeo():
    result1 = subprocess.run(
        [sys.executable, "-m", "temperatura", "1.0027777777777777777777777777", "C", "F"],
        capture_output=True,
        text=True,
    )
    assert result1.returncode == 0
    assert result1.stdout.strip() == "33.80 F"

    result2 = subprocess.run(
        [sys.executable, "-m", "temperatura", "1.0027777777777777777777777778", "C", "F"],
        capture_output=True,
        text=True,
    )
    assert result2.returncode == 0
    assert result2.stdout.strip() == "33.81 F"
