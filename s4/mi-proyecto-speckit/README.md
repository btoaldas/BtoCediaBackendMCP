# Conversor de temperatura — base P3

Versión creada mediante el flujo Specify, Plan, Tasks e Implement de Spec Kit con agy. Conserva la etapa de P3 con 55 pruebas. Las mejoras de QA se registran después en P4. El snapshot idéntico de código se conserva en `../versiones/p3-base-55`.

Desde este directorio:

```bash
uv sync --frozen
uv run --frozen pytest tests/ -q
uv run --frozen python -m temperatura 0 C F
uv run --frozen python -m temperatura -273.15 C K
uv run --frozen python -m temperatura NaN C F
```

Resultados: 32.00 F y 0.00 K con salida 0; NaN es rechazado con salida 2. Los documentos de requisitos, arquitectura y tareas están en `specs/001-conversor-temperatura`. Ver `../comparacion.md` y la versión manual `../clase-sdd`.

Límite histórico: la base55 conserva dos problemas encontrados posteriormente en P4 (exponentes fuera de rango y doble redondeo). Su finalidad es reproducir la etapa evaluada, no representar la versión corregida final.
