# Resultados históricos 3.B — base P3 de 55 pruebas

Este registro corresponde a P3. La [versión final P4](README.md) tiene 65 pruebas y 94,3 % de cobertura; véase el [reporte final](reporte-qa.html). La [base P3](../versiones/p3-base-55/README.md) se conserva separada para reproducir los resultados siguientes.

Se inicializó Specify CLI desde el repositorio oficial `github/spec-kit`, commit
`c173bf19a6654e3b05386ec3599349a55282b897`, usando la integración `agy`.
En la TUI real de agy se ejecutó `/speckit-specify`, `/speckit-plan`,
`/speckit-tasks` y `/speckit-implement`. Cada fase produjo archivos y se
conservó un snapshot antes de avanzar. No se simuló la herramienta.

El flujo produjo tres historias, 18 escenarios, 13 requisitos funcionales y
33 tareas. La implementación usa Python 3.12, aritmética Decimal, CLI separada
del dominio y tres capas de pruebas.

| Caso | Comando desde esta carpeta | stdout | Exit |
|---|---|---|---|
| Normal | `uv run python -m temperatura 0 C F` | `32.00 F` | 0 |
| Borde | `uv run python -m temperatura -273.15 C K` | `0.00 K` | 0 |
| No contemplado en spec manual | `uv run python -m temperatura NaN C F` | vacío; error controlado en stderr | 2 |

Estos son exactamente los tres casos de 3.A. La comparación y su limitación
metodológica están en [comparacion.md](../comparacion.md).

## Verificación de la implementación base P3

La suite real de agy terminó con **55 aprobadas**: 19 unitarias, 27 de integración
en memoria y nueve e2e. La cobertura de esa corrida fue **108/122 líneas
(88,52 %, mostrado como 89 %)**. Los subprocesos e2e prueban el comportamiento,
pero sus líneas no se suman a la medición de cobertura de este comando.

Un proceso e2e detectó inicialmente `No module named temperatura`. Una revisión
independiente encontró que el arreglo local con editable no bastaba para un
entorno nuevo. El mismo agy corrigió el empaquetado declarando
`setuptools.build_meta`, descubrimiento de paquetes en `src` y actualización
del lock. Codex repitió después, en otro entorno recién creado:

```bash
UV_PROJECT_ENVIRONMENT=.tmp/entornos-verificacion/<id-nuevo> uv sync --frozen
UV_PROJECT_ENVIRONMENT=.tmp/entornos-verificacion/<id-nuevo> uv run --frozen python -m temperatura 0 C F
UV_PROJECT_ENVIRONMENT=.tmp/entornos-verificacion/<id-nuevo> uv run --frozen pytest tests/ -q
```

Resultado: instalación exit 0; CLI `32.00 F` exit 0; **55 aprobadas en 0,27 s**.
Los estados fallidos y las intervenciones no se ocultan. Véase
[incidencias verificadas](../../docs/p03-p04/incidencias-verificadas.md).

P4 continúa este código y puede ampliar sus pruebas. Los conteos de este
archivo corresponden a la base P3 conservada en `08-p3-reproducible`.
