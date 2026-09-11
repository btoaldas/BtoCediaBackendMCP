# Implementation Plan: Conversor de Temperatura CLI

**Branch**: `001-conversor-temperatura` | **Date**: 2026-09-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-conversor-temperatura/spec.md`

---

## Summary

Implementar un conversor de temperaturas por línea de comandos entre las escalas Celsius, Fahrenheit y Kelvin usando Python 3.12 estándar y `uv`. El sistema garantiza alta precisión matemática y redondeo aritmético determinista mediante `decimal.Decimal` (`ROUND_HALF_UP`), valida rigurosamente los límites del cero absoluto (-273.15 °C, -459.67 °F, 0 K), rechaza de forma defensiva entradas superiores a 32 caracteres, cadenas no numéricas, literales especiales (`NaN`/`Infinity`) y magnitudes excesivas ($> 1.0 \times 10^{12}$).

La arquitectura separa la lógica pura de dominio (`src/temperatura/dominio.py`) del controlador de interfaz CLI (`src/temperatura/cli.py` y `src/temperatura/__main__.py`) para permitir la ejecución modular vía `python -m temperatura` y asegurar una estrategia de verificación en tres capas independientes: pruebas unitarias de dominio, integración CLI en memoria y pruebas de subproceso end-to-end.

---

## Technical Context

**Language/Version**: Python 3.12 (gestionado con `uv`).

**Primary Dependencies**: Biblioteca estándar de Python (`decimal`, `sys`, `typing`, `enum`). Cero dependencias externas en producción.

**Storage**: N/A (herramienta CLI sin estado ni persistencia en disco).

**Testing**: `pytest` distribuido en tres capas especializadas (`tests/unit`, `tests/integration`, `tests/e2e`).

**Target Platform**: CLI multiplataforma estándar (macOS / Linux / POSIX).

**Project Type**: Paquete de biblioteca modular con interfaz de línea de comandos (`src/temperatura`).

**Performance Goals**: Tiempo de inicio y respuesta en frío inferior a 200 ms por consulta.

**Constraints**: Ejecución local 100% desconectada (sin red ni base de datos), límite de 32 caracteres en cadena de entrada antes de procesamiento, normalización de cero negativo exclusivamente cuando el resultado cuantitativo redondeado sea nulo, códigos de salida estrictos (`0` éxito, `2` error de entrada o validación).

**Scale/Scope**: 3 módulos de código en `src/temperatura/`, 3 suites de pruebas automatizadas y soporte de notación decimal y científica estándar (e.g. `-1e2`).

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio Constitucional | Estado | Justificación / Mecanismo de Cumplimiento |
|---|:---:|---|
| **I. Library-First** | **PASS** | El dominio matemático (`temperatura.dominio`) es autónomo y desacoplado; puede utilizarse como biblioteca independiente sin invocar la CLI ni requerir streams de terminal. |
| **II. CLI Interface** | **PASS** | Implementación de `temperatura.cli` y `__main__.py` siguiendo el protocolo de texto estándar: `stdout` para resultados exactos con código `0`, `stderr` para diagnósticos claros con código `2`. |
| **III. Test-First (TDD)** | **PASS** | Casos de aceptación definidos formalmente antes de codificación, estructurados para verificación automatizada con `pytest`. |
| **IV. Multi-Layer Testing** | **PASS** | 3 capas desacopladas: unidad matemática pura, integración CLI en memoria con `capsys`, y E2E mediante `subprocess.run`. |
| **V. Simplicity & YAGNI** | **PASS** | Implementación apoyada exclusivamente en `stdlib` y `Decimal`, sin dependencias pesadas, sin capas ORM ni llamadas a red. |

---

## Project Structure

### Documentation (this feature)

```text
specs/001-conversor-temperatura/
├── plan.md              # Este plan de implementación
├── research.md          # Fase 0: Decisiones técnicas, aritmética Decimal y arquitectura
├── data-model.md        # Fase 1: Entidades de dominio, invariantes y excepciones
├── quickstart.md        # Fase 1: Guía de ejecución rápida y validación de extremo a extremo
├── contracts/
│   └── cli-contract.md  # Fase 1: Especificación formal de argumentos, streams y códigos de salida
└── checklists/
    └── requirements.md  # Checklist de calidad de requisitos
```

### Source Code (repository layout)

```text
src/
└── temperatura/
    ├── __init__.py
    ├── __main__.py      # sys.exit(main()) para python -m temperatura
    ├── cli.py           # Parser ligero de argumentos, manejo de streams y exit codes
    └── dominio.py       # Escala, LecturaTemperatura, ResultadoConversion, fórmulas puras

tests/
├── __init__.py
├── unit/
│   └── test_dominio.py         # Capa 1: Pruebas unitarias de fórmulas y cero absoluto
├── integration/
│   └── test_cli_memoria.py     # Capa 2: Pruebas de integración CLI en memoria (capsys)
└── e2e/
    └── test_cli_subprocess.py  # Capa 3: Pruebas End-to-End invocando subprocesos reales
```

**Structure Decision**: Se adopta una disposición modular limpia donde `src/temperatura` aísla las reglas de negocio en `dominio.py` y la interacción con el sistema en `cli.py` y `__main__.py`. Las pruebas bajo `tests/` reflejan fielmente las tres capas solicitadas sin redundancias ni dependencias cruzadas.

---

## Complexity Tracking

> *No existen desviaciones ni violaciones a las reglas constitucionales. El diseño se mantiene estrictamente minimalista y conforme a los principios establecidos.*

| Violación | Por qué se necesita | Alternativa más simple descartada porque |
|---|---|---|
| *Ninguna* | *N/A* | *N/A* |
