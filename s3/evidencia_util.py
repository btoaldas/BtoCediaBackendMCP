"""Carga snapshots inmutables para pruebas, sin tocar reglas generadas."""
import importlib.util
from pathlib import Path
import sys


def cargar(nombre):
    ruta = Path(__file__).parent / "rondas" / nombre / "main.py"
    key = "snapshot_" + nombre.replace("-", "_")
    spec = importlib.util.spec_from_file_location(key, ruta)
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module
