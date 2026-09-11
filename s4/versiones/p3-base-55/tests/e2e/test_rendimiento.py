"""Pruebas de rendimiento en frío para la CLI (SC-004)."""

import subprocess
import sys
import time


def test_sc004_rendimiento_en_frio_ejecutable_python():
    """Mide el tiempo de arranque y ejecución en frío con el intérprete Python directo (aislando uv)."""
    inicio = time.perf_counter()
    result = subprocess.run(
        [sys.executable, "-m", "temperatura", "100", "C", "F"],
        capture_output=True,
        text=True,
    )
    duracion = time.perf_counter() - inicio

    assert result.returncode == 0
    assert result.stdout.strip() == "212.00 F"
    # Requisito SC-004: tiempo de respuesta inferior a 200 ms (0.2 s)
    assert duracion < 0.200, f"Tiempo de ejecución ({duracion:.4f}s) superó el umbral de 200ms"
