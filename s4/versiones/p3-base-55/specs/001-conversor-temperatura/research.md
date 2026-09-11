# Phase 0 Research: Conversor de Temperatura CLI

**Feature**: [spec.md](spec.md)
**Date**: 2026-09-10
**Status**: Completed

El presente documento consolida la investigación técnica y las decisiones de arquitectura para resolver los requerimientos de precisión, límites físicos, contratos CLI y verificación en múltiples capas del conversor de temperatura.

---

## 1. Precisión Numérica y Estrategia de Redondeo

### Contexto
Las conversiones entre Celsius, Fahrenheit y Kelvin requieren divisiones racionales periódicas ($\frac{5}{9}$ y $\frac{9}{5}$) y desplazamientos aditivos ($32$ y $273.15$). En aritmética binaria de coma flotante (`float`), valores como $273.15$ o las fracciones de tercio no tienen representación binaria finita exacta, lo que genera errores de representación y redondeos inconsistentes en los umbrales de corte (por ejemplo, `-459.67` en Fahrenheit o el cero absoluto).

### Decision
Utilizar exclusivamente `decimal.Decimal` de la biblioteca estándar de Python (`stdlib`) con la política de redondeo `decimal.ROUND_HALF_UP` para toda la lógica interna de validación, conversión y formateo a dos decimales (`Decimal('0.01')`).

### Rationale
- `Decimal` opera en base 10 exacta, eliminando errores de aproximación binaria en constantes físicas como `273.15` y `459.67`.
- `ROUND_HALF_UP` implementa de forma determinista el redondeo aritmético convencional requerido por las especificaciones de usuario (los empates a 5 siempre redondean alejándose de cero, a diferencia del *round-to-even* bancario por defecto en Python).
- Facilita la comparación estricta de umbrales: `valor < escala.cero_absoluto` sin tolerancias arbitrarias de coma flotante (`epsilon`).

### Alternatives Considered
- **`float` estándar de Python**: Descartado debido a imprecisiones de representación IEEE 754 binarias que provocan fallos de aserción en comparaciones exactas de frontera como `-459.67` o en redondeos de valores con cola decimal periódica.
- **`fractions.Fraction`**: Aunque ofrece precisión matemática infinita para números racionales, introduce complejidad innecesaria en la serialización y formateo decimal final en comparación con `Decimal`.

---

## 2. Manejo Semántico de Cero con Signo y Normalización de Salida

### Contexto
El requerimiento establece: *"Interpretación de cero con signo: solo normalizar a 0.00 cuando RESULTADO redondeado sea cero, no convertir 0 C F a cero."*

En aritmética de coma flotante y en `Decimal`, un valor negativo cercano a cero puede cuantizarse como `-0.00`. Se debe garantizar que la salida visual no presente el signo negativo si la magnitud cuantitativa es nula (`-0.00` → `0.00`), pero sin alterar en ningún momento conversiones legítimas donde la entrada es `0` y el resultado es no nulo (como `0 C` a Fahrenheit, que debe ser exactamente `32.00 F`).

### Decision
Aplicar la normalización de signo exclusivamente sobre el valor final cuantizado/redondeado mediante inspección semántica:
```python
resultado_cuantizado = valor_calculado.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
if resultado_cuantizado.is_zero():
    resultado_cuantizado = Decimal('0.00')
```

### Rationale
- Se preserva la semántica matemática de la conversión: `0 C` a `F` calcula `32.00 F`, mientras que `-0.001 C` a `C` o `0 C` a `C` cuantiza a `0.00 C`.
- Evita condiciones de carrera en formateo de texto o transformaciones ciegas de cadenas que pudieran corromper representaciones con signo legítimas.

### Alternatives Considered
- **Reemplazo simple de cadena (`replace("-0.00", "0.00")`)**: Aunque funciona superficialmente, delegar la normalización a nivel de objeto `Decimal` en el dominio matemático es más robusto y desacoplado de la capa de presentación.
- **Normalizar la entrada a cero antes de convertir**: Descartado rotundamente porque transformaría entradas como `0 C` en un cero arbitrario en lugar de calcular su valor real en Fahrenheit (`32.00 F`) o Kelvin (`273.15 K`).

---

## 3. Validación Previa de Longitud, Notación Científica y Literales Especiales

### Contexto
Se requiere:
- Rechazo explícito de entradas vacías y no numéricas con salida legible y código de salida 2.
- Límite de 32 caracteres en la cadena de entrada evaluado antes de cualquier procesamiento pesado.
- Aceptación de notación científica válida como `-1e2` dentro del contrato numérico.
- Rechazo estricto de literales de punto flotante (`NaN`, `Infinity`, `inf`, etc.).
- Rechazo de magnitudes excesivas ($|T| > 1.0 \times 10^{12}$).

### Decision
1. **Límite de longitud previo**: Evaluar `len(raw_input.strip()) <= 32` como primer paso defensivo. Si la longitud excede 32 caracteres, rechazar de inmediato con error descriptivo y código 2.
2. **Filtro de literales especiales**: Comprobar de forma insensible a mayúsculas/minúsculas si la cadena depurada contiene o coincide con `"nan"`, `"inf"`, `"-inf"`, `"infinity"` antes de instanciar `Decimal`.
3. **Conversión segura a Decimal**: Intentar construir `Decimal(raw_input)`. `Decimal` soporta de manera nativa notación científica estándar (como `-1e2`, `1.5e3`), convirtiéndolos a valores decimales exactos (`-100`, `1500`).
4. **Validación de finitud y magnitud**: Verificar que el valor resultante no sea `is_nan()` ni `is_infinite()`, y validar que `abs(valor) <= Decimal('1e12')`.

### Rationale
- El límite temprano de 32 caracteres previene ataques de denegación de servicio por cadenas monstruosas o entradas malformadas.
- La exclusión previa de `nan` e `inf` evita que `Decimal` los interprete como números válidos del dominio físico.
- Soportar `-1e2` cumple con la necesidad científica sin relajar las restricciones de seguridad ni de rango físico.

### Alternatives Considered
- **Expresiones regulares complejas para parsing numérico**: Propenso a errores en dialectos de regex y menos legible que la combinación de un filtro de exclusión de cadenas más la conversión directa con manejo de `InvalidOperation`.
- **`float(raw_input)` como validador**: Descartado porque introduce `nan` e `inf` sin lanzar excepción y pierde precisión en valores límite.

---

## 4. Arquitectura Modular del Paquete

### Contexto
El usuario exige un paquete en `src/temperatura` con `dominio.py`, `cli.py`, `__main__.py`, ejecutable vía `python -m temperatura`.

### Decision
Estructurar el código bajo una estricta separación de responsabilidades:
- **`src/temperatura/dominio.py`**:
  - `Escala` (Enum: `CELSIUS = 'C'`, `FAHRENHEIT = 'F'`, `KELVIN = 'K'`).
  - `LecturaTemperatura` y `ResultadoConversion` (Value Objects inmutables con validación de límites físicos).
  - Funciones puras de cálculo: `convertir(valor: Decimal, escala_origen: Escala, escala_destino: Escala) -> ResultadoConversion`.
  - Excepciones tipadas: `ErrorTemperatura`, `ErrorCeroAbsoluto`, `ErrorEntradaInvalida`.
- **`src/temperatura/cli.py`**:
  - Función `main(argv: list[str] | None = None) -> int`:
    - Valida longitud y número de argumentos.
    - Sanitiza cadenas de entrada.
    - Atrapa excepciones de dominio y emite mensajes legibles a `sys.stderr`.
    - En caso de éxito, escribe el resultado en `sys.stdout` y retorna `0`.
    - En caso de error de validación o entrada, retorna `2`.
- **`src/temperatura/__main__.py`**:
  - Invoca `sys.exit(main())` para habilitar `python -m temperatura`.

### Rationale
Cumple el principio *Library-First* de la constitución: la lógica de dominio es 100% testeable sin depender de flujos de E/S ni de la CLI, mientras que la CLI se encarga del protocolo de entrada/salida y códigos de salida de proceso.

---

## 5. Estrategia de Pruebas en Tres Capas

### Contexto
Se requiere verificar el sistema en tres capas no redundantes:
1. Unidad lógica aislada.
2. Integración CLI-dominio en memoria.
3. End-to-end mediante subproceso real.

### Decision
Implementar las suites en directorios dedicados bajo `tests/`:
1. **`tests/unit/test_dominio.py`**:
   - Pruebas directas de funciones matemáticas de conversión entre todos los pares (C↔F, C↔K, F↔K).
   - Pruebas de umbrales exactos de cero absoluto y rechazo de valores inferiores.
   - Pruebas de normalización de `-0.00` a `0.00` en resultados cuantizados.
2. **`tests/integration/test_cli_memoria.py`**:
   - Invocación de `cli.main(argv)` pasando listas de strings.
   - Captura de `capsys` (stdout y stderr) y verificación de códigos de retorno (`0` o `2`).
   - Prueba el flujo completo de validación de strings, manejo de excepciones y formato sin crear procesos del sistema operativo.
3. **`tests/e2e/test_cli_subprocess.py`**:
   - Ejecución real del comando mediante `subprocess.run([sys.executable, "-m", "temperatura", ...])`.
   - Verifica el comportamiento del proceso en el sistema operativo, propagación de exit codes, streams y compatibilidad de ejecución con `python -m temperatura`.

### Rationale
Cada capa cubre un nivel de abstracción distinto sin duplicar esfuerzos ni omitir escenarios de integración con el entorno.

---

## 6. Gestión de Entorno y Gobernanza

### Decision
- **Lenguaje**: Python 3.12 exclusivamente.
- **Herramienta de entorno y paquetes**: `uv` con entorno virtual estándar.
- **Dependencias de producción**: Cero dependencias externas (`stdlib` pura).
- **Dependencias de desarrollo**: `pytest`.
- **Red y Persistencia**: Estrictamente desconectado; no requiere bases de datos, APIs de red ni archivos externos persistentes.
