# Bloque 3.A — Spec manual

La implementación evaluada es `conversor_agy.py`, código devuelto por una llamada
real a `agy --print` que recibió `spec_manual.md` completo. Codex guardó el bloque
Python sin cambios y ejecutó las pruebas. Ejecutar:

```bash
uv run python conversor_agy.py 0 C F
uv run python conversor_agy.py -273.15 C K
uv run python conversor_agy.py NaN C F
```

Los dos primeros comandos producen `32.00 F` y `0.00 K`, respectivamente, con
exit 0. El tercero rechaza el valor con mensaje en stderr y exit 2. Véase
[resultados-3a.md](resultados-3a.md) para la evidencia y la intervención declarada.

`conversor.py` conserva el borrador previo preparado con Codex durante el bloqueo
de autenticación. No se cuenta como la implementación producida por agy.
