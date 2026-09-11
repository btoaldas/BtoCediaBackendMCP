# Tasks: Conversor de Temperatura CLI

**Input**: Design documents from `specs/001-conversor-temperatura/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/cli-contract.md`, `quickstart.md`)

**Prerequisites**:
- `plan.md` (arquitectura de paquetes, dependencias stdlib, pruebas en 3 capas)
- `spec.md` (historias de usuario P1, P2, P3, requisitos FR-001 a FR-013, criterios SC-001 a SC-004, edge cases)
- `research.md` (decisiones de precisión `Decimal`, `ROUND_HALF_UP`, normalización de cero negativo)
- `data-model.md` (entidades `Escala`, `LecturaTemperatura`, `ResultadoConversion`, excepciones)
- `contracts/cli-contract.md` (esquema CLI, streams stdout/stderr, códigos de salida 0 y 2)
- **Nota de Gobernanza**: La constitución del proyecto en `.specify/memory/constitution.md` es una plantilla referencial sin ratificar; los principios expuestos en el plan corresponden a principios de diseño propuestos para esta funcionalidad. No se asume una constitución formalmente aprobada ni pruebas pasadas con antelación.

**Tests**: Se adopta un enfoque Test-First riguroso: las pruebas de aceptación (capas unitaria, integración en memoria y e2e por subproceso) se codifican antes de la implementación y deben pasar por una ejecución roja (RED) observable previa a la implementación.

**Organization**: Tareas agrupadas por fases y por historia de usuario para garantizar incrementos independientes y testeables.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Ejecutable en paralelo (archivos independientes sin bloqueos)
- **[Story]**: Etiqueta de historia de usuario (`[US1]`, `[US2]`, `[US3]`) aplicada exclusivamente en las fases de historias
- Cada tarea incluye la ruta de archivo exacta correspondiente

---

## Path Conventions

- Código fuente: `src/temperatura/` (`__init__.py`, `__main__.py`, `cli.py`, `dominio.py`)
- Suites de pruebas: `tests/` (`unit/`, `integration/`, `e2e/`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicialización del proyecto, estructura de directorios y entorno de pruebas con Python 3.12 y `uv`.

- [X] T001 Crear la estructura de directorios del paquete y las tres capas de pruebas en src/temperatura/, tests/unit/, tests/integration/ y tests/e2e/
- [X] T002 [P] Configurar pyproject.toml con configuración de proyecto Python 3.12, herramientas uv y runner de pruebas pytest en pyproject.toml
- [X] T003 [P] Crear módulos de inicialización vacíos en src/temperatura/__init__.py y tests/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Componentes base de dominio y punto de entrada que bloquean la implementación de las historias de usuario.

**⚠️ CRITICAL**: Completar esta fase antes de iniciar el ciclo TDD de las historias de usuario.

- [X] T004 Implementar la jerarquía de excepciones de dominio ErrorTemperatura(Exception), ErrorCeroAbsoluto(ErrorTemperatura) y ErrorEntradaInvalida(ErrorTemperatura) en src/temperatura/dominio.py
- [X] T005 [P] Implementar la enumeración Escala en src/temperatura/dominio.py con valores CELSIUS='C', FAHRENHEIT='F', KELVIN='K', atributos cero_absoluto (Decimal('-273.15'), Decimal('-459.67'), Decimal('0.0')) y método de clase desde_simbolo(simbolo: str) con validación estricta y descarte de unidades inválidas
- [X] T006 [P] Implementar el punto de entrada ejecutable del paquete en src/temperatura/__main__.py invocando sys.exit(main()) desde src/temperatura/cli.py

**Checkpoint**: Base lista — las historias de usuario pueden comenzar con su ciclo TDD independiente.

---

## Phase 3: User Story 1 - Conversión Estándar entre Escalas de Temperatura (Priority: P1) 🎯 MVP

**Goal**: Conversión bidireccional exacta entre Celsius, Fahrenheit y Kelvin desde CLI, con preservación de valor en misma escala, aceptación de negativos físicamente válidos, salida con formato `<valor:.2f> <UNIDAD>` en stdout y código de salida 0 (FR-001, FR-002, FR-003, FR-004, FR-005, FR-008, SC-001).

**Independent Test**: Ejecutar conversiones válidas para todos los pares (100 C F -> 212.00 F, 212 F C -> 100.00 C, 0 C K -> 273.15 K, 373.15 K C -> 100.00 C, 32 F K -> 273.15 K, 273.15 K F -> 32.00 F), misma unidad (25 C C -> 25.00 C) y negativo válido (-40 C F -> -40.00 F), verificando formato y exit code 0.

### Tests for User Story 1 (Write FIRST, observe initial RED execution) ⚠️

- [X] T007 [P] [US1] Escribir pruebas unitarias de fórmulas de conversión y preservación de valor en tests/unit/test_dominio.py
- [X] T008 [P] [US1] Escribir pruebas de integración en memoria para invocaciones CLI exitosas y formateo de stdout en tests/integration/test_cli_memoria.py
- [X] T009 [P] [US1] Escribir pruebas end-to-end con subprocess.run para ejecución real vía python -m temperatura en tests/e2e/test_cli_subprocess.py
- [X] T010 [US1] Ejecución roja inicial observable: correr pytest tests/ -k "US1" y confirmar fallo esperado antes de implementar

### Implementation for User Story 1

- [X] T011 [US1] Implementar objetos de valor LecturaTemperatura y ResultadoConversion en src/temperatura/dominio.py con cuantización Decimal('0.01') y política ROUND_HALF_UP
- [X] T012 [US1] Implementar la función de cálculo matemático puro convertir(valor: Decimal, escala_origen: Escala, escala_destino: Escala) -> ResultadoConversion en src/temperatura/dominio.py
- [X] T013 [US1] Implementar en src/temperatura/cli.py la función main(argv=None) para procesar argumentos posicionales válidos, emitir el resultado formateado a sys.stdout y retornar 0
- [X] T014 [US1] Verificación verde: ejecutar pytest tests/ -k "US1" y certificar que todas las pruebas de US1 pasan exitosamente

**Checkpoint**: MVP operativo. Las conversiones válidas y el formato estándar funcionan y se prueban independientemente.

---

## Phase 4: User Story 2 - Validación de Límites Físicos y Cero Absoluto (Priority: P2)

**Goal**: Rechazar temperaturas inferiores al cero absoluto de la escala de origen (-273.15 °C, -459.67 °F, 0 K) con mensaje descriptivo en stderr y código de salida 2; aceptar y convertir correctamente los valores en el umbral exacto (FR-006, FR-007, SC-002).

**Independent Test**: Probar valores < cero absoluto (-273.16 C, -459.68 F, -1 K) constatando mensaje en stderr y código 2; probar umbrales exactos (-273.15 C K -> 0.00 K, 0 K C -> -273.15 C) con código 0.

### Tests for User Story 2 (Write FIRST, observe initial RED execution) ⚠️

- [X] T015 [P] [US2] Escribir pruebas unitarias para validación del cero absoluto y aceptación de umbrales exactos en tests/unit/test_dominio.py
- [X] T016 [P] [US2] Escribir pruebas de integración en memoria para captura de ErrorCeroAbsoluto en stderr y retorno 2 en tests/integration/test_cli_memoria.py
- [X] T017 [P] [US2] Escribir pruebas end-to-end con subprocess.run para rechazo de temperaturas bajo el cero absoluto en tests/e2e/test_cli_subprocess.py
- [X] T018 [US2] Ejecución roja inicial observable: correr pytest tests/ -k "US2" y confirmar fallo esperado antes de implementar

### Implementation for User Story 2

- [X] T019 [US2] Incorporar regla de validación de cero absoluto valor >= escala.cero_absoluto en LecturaTemperatura en src/temperatura/dominio.py lanzando ErrorCeroAbsoluto
- [X] T020 [US2] Conectar la captura de ErrorCeroAbsoluto en src/temperatura/cli.py para imprimir mensaje en sys.stderr y retornar código de salida 2
- [X] T021 [US2] Verificación verde: ejecutar pytest tests/ -k "US2" y certificar que las pruebas de cero absoluto pasan exitosamente

**Checkpoint**: Integridad termodinámica garantizada. US1 y US2 son verificables de manera combinada e independiente.

---

## Phase 5: User Story 3 - Manejo Robusto de Entradas No Numéricas, Especiales y Extremas (Priority: P3)

**Goal**: Validar defensivamente las entradas CLI, rechazando argumentos insuficientes o vacíos, caracteres no numéricos, literales de punto flotante (NaN, Infinity), cadenas > 32 caracteres, magnitudes > 1.0e12 y unidades desconocidas, emitiendo mensaje claro en stderr y finalizando con código 2 sin caídas imprevistas (FR-009, FR-010, FR-011, FR-012, FR-013, SC-003).

**Independent Test**: Invocar la CLI con "", "abc", "nan", "Infinity", cadena de 33 caracteres, "1e13", "100 X F" y verificar que todas retornan código 2 con mensaje en stderr y sin traza técnica de excepción.

### Tests for User Story 3 (Write FIRST, observe initial RED execution) ⚠️

- [X] T022 [P] [US3] Escribir pruebas unitarias para restricciones de entrada (len > 32, rechazo nan/inf, magnitud > 1e12, unidades inválidas) en tests/unit/test_dominio.py
- [X] T023 [P] [US3] Escribir pruebas de integración en memoria para validación de argumentos en CLI (falta de argumentos, no numéricos, error legible) en tests/integration/test_cli_memoria.py
- [X] T024 [P] [US3] Escribir pruebas end-to-end con subprocess.run para entradas malformadas, aceptación de -1e2 y código de salida 2 en tests/e2e/test_cli_subprocess.py
- [X] T025 [US3] Ejecución roja inicial observable: correr pytest tests/ -k "US3" y confirmar fallo esperado antes de implementar

### Implementation for User Story 3

- [X] T026 [US3] Implementar en src/temperatura/cli.py la validación previa de longitud len(raw_input) <= 32 (evaluada ANTES de strip) y filtrado insensible a mayúsculas de nan, inf e infinity antes de la conversión numéríca
- [X] T027 [US3] Implementar en src/temperatura/dominio.py la conversión segura a Decimal, validación de magnitud abs(valor) <= Decimal('1e12') y validación de finitud
- [X] T028 [US3] Estructurar el manejador global de excepciones en src/temperatura/cli.py para capturar ErrorEntradaInvalida y errores de invocación, emitiendo mensaje a sys.stderr y retornando 2
- [X] T029 [US3] Verificación verde: ejecutar pytest tests/ -k "US3" y certificar que la validación robusta y segura pasa al 100%

**Checkpoint**: Sistema blindado ante entradas anómalas. Todas las historias de usuario (US1, US2, US3) funcionan de forma independiente e integrada.

---

## Phase 6: Edge Cases, Performance & Polish (Cross-Cutting Concerns)

**Purpose**: Validación exhaustiva de casos límite especificados, medición de rendimiento en frío y verificación completa de la guía quickstart.

- [X] T030 [P] Escribir pruebas de casos de borde en tests/unit/test_dominio.py y tests/integration/test_cli_memoria.py cubriendo normalización de -0.00 a 0.00 exclusivamente cuando el resultado cuantizado sea nulo (sin alterar 0 C F -> 32.00 F), redondeo ROUND_HALF_UP en 25.555 -> 25.56, saneamiento de espacios circundantes y punto de corte exacto -459.67 F vs -459.671 F
- [X] T031 Refinar el formateo en src/temperatura/dominio.py asegurando que si cuantizado.is_zero() es True se devuelva Decimal('0.00') manteniendo inalterados los resultados no nulos
- [X] T032 [P] Implementar prueba de rendimiento en frío en tests/e2e/test_rendimiento.py midiendo el tiempo de arranque y respuesta con el intérprete Python directo (sys.executable -m temperatura 100 C F, excluyendo la sobrecarga inicial de uv) y asegurando tiempo < 200 ms (SC-004)
- [X] T033 Ejecutar la suite completa en las tres capas (pytest tests/) y verificar los escenarios documentados en specs/001-conversor-temperatura/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)**: Sin dependencias — inicio inmediato.
2. **Foundational (Phase 2)**: Depende de Phase 1 — BLOQUEA todas las historias de usuario.
3. **User Story 1 (Phase 3)**: Depende de Phase 2. MVP funcional.
4. **User Story 2 (Phase 4)**: Depende de Phase 2 (se integra con US1).
5. **User Story 3 (Phase 5)**: Depende de Phase 2 (completa el blindaje de US1 y US2).
6. **Polish (Phase 6)**: Depende de la finalización de US1, US2 y US3.

### Reglas de Ejecución Dentro de Cada Historia

- Las tareas de prueba (`Tests`) se escriben primero y se ejecuta la verificación roja inicial (RED).
- Se implementan los modelos/dominio antes de la CLI.
- Se ejecuta la verificación verde (GREEN) antes de declarar completa la historia.

### Parallel Opportunities

- **Fase 1**: T002 y T003 pueden ejecutarse en paralelo tras T001.
- **Fase 2**: T005 y T006 pueden desarrollarse en paralelo con T004.
- **Fases de Pruebas**: En cada historia, los tests unitarios, de integración en memoria y e2e ([P]) se pueden escribir concurrentemente antes de la corrida roja.
- **Fase 6**: T030 y T032 pueden ejecutarse en paralelo.

---

## Parallel Example: User Story 1

```bash
# Escribir en paralelo las pruebas de US1 para las 3 capas:
Task T007: "tests/unit/test_dominio.py"
Task T008: "tests/integration/test_cli_memoria.py"
Task T009: "tests/e2e/test_cli_subprocess.py"

# Ejecutar corrida roja inicial observable:
Task T010: "pytest tests/ -k 'US1'"
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Completar Setup (Fase 1) y Foundational (Fase 2).
2. Ejecutar Fase 3 (US1) completa: tests TDD → corrida roja → implementación → corrida verde.
3. **Pausa y validación**: Verificar conversión funcional básica con `python -m temperatura 100 C F`.

### Entrega Incremental

1. Base + Setup listos.
2. Añadir US1 (Conversiones estándar) → MVP probado.
3. Añadir US2 (Límites termodinámicos y cero absoluto) → Validado sin romper US1.
4. Añadir US3 (Defensa ante NaN, cadenas largas y caracteres no numéricos) → Sistema blindado.
5. Fase 6: Casos de borde, redondeo estricto y prueba de rendimiento en frío < 200 ms (SC-004).

---

## Notes

- Cada tarea cumple la convención `- [ ] [TaskID] [P?] [Story?] Descripción con ruta de archivo`.
- Las tres capas de pruebas están desacopladas y no duplican responsabilidades:
  - `tests/unit/`: Lógica matemática y constantes.
  - `tests/integration/`: Argumentos, captura `capsys` en memoria y códigos de retorno.
  - `tests/e2e/`: Ejecución por subproceso real del sistema operativo (`python -m temperatura`).
- Medición de rendimiento en frío aislada al intérprete Python sin penalización del runtime de `uv`.
