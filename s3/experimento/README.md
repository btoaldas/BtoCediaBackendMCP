# Entorno del experimento de la práctica 2

Este entorno Python 3.12 y uv permite reproducir las cuatro rondas generadas por agy y sus comprobaciones, sin volver a llamar a un servicio de IA.

Los comandos y resultados esperados están en [la guía definitiva de reproducción](../README.md). Se ejecutan desde la raíz del repositorio mediante `uv run --project s3/experimento python s3/probar_ronda_01.py`, cambiando el script según la ronda.

`pyproject.toml`, `.python-version` y `uv.lock` conservan la configuración del entorno. Los snapshots evaluados viven en `s3/rondas/01-contrasenas` a `04-administradores`; el fallo intencional de administradores se conserva como evidencia del ejercicio y debe terminar con exit 1.
