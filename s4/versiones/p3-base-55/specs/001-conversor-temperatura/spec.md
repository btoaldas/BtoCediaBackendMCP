# Feature Specification: Conversor de Temperatura CLI

**Feature Branch**: `001-conversor-temperatura`

**Created**: 2026-09-10

**Status**: Draft

**Input**: User description: "Convertir una temperatura entre Celsius, Fahrenheit y Kelvin desde CLI. Aceptar valor y unidades C/F/K sin distinguir mayúsculas. Convertir C↔F, C↔K y F↔K correctamente. Presentar exactamente dos decimales y unidad destino. Rechazar valores bajo cero absoluto (-273.15 C, -459.67 F y 0 K). Entradas vacías o no numéricas producen error legible exit 2; éxito exit 0. Mismas unidades conserva valor; negativos físicamente válidos se aceptan. Añadir decisiones explícitas para NaN/Infinity y magnitud/longitud excesivas. Proyecto laboratorio Python 3.12 stdlib con uv. Sigue la skill real instalada. No crees ni cambies ramas Git ni commits ni remotos: usa SPECIFY_FEATURE=001-conversor-temperatura y crea artefactos bajo specs/001-conversor-temperatura sin alterar Git padre; si script requiere Git no lo ejecutes sin opción de omitirlo. No borres archivos, no accedas a carpetas hermanas ni credenciales. Tu alcance es esta carpeta."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conversión Estándar entre Escalas de Temperatura (Priority: P1)

Como usuario de línea de comandos, deseo convertir valores de temperatura entre las escalas Celsius (C), Fahrenheit (F) y Kelvin (K) especificando el valor numérico, la unidad de origen y la unidad de destino, para obtener el valor convertido exacto con dos decimales y su unidad correspondiente.

**Why this priority**: Es la funcionalidad central y el valor primordial de la herramienta; permite calcular de manera confiable las conversiones directas e inversas entre las tres escalas principales, así como preservar el valor cuando las unidades origen y destino coinciden.

**Independent Test**: Puede probarse de manera aislada ejecutando conversiones válidas entre cada par de escalas (C↔F, C↔K, F↔K) y comprobando que la salida estándar muestra exactamente dos decimales y la unidad destino en mayúscula con código de salida 0.

**Acceptance Scenarios**:

1. **Given** un usuario que requiere convertir 100 °C a Fahrenheit, **When** invoca la CLI con `100 C F` (o minúsculas `100 c f`), **Then** la CLI responde con `212.00 F` en stdout y código de salida 0.
2. **Given** un usuario que requiere convertir 212 °F a Celsius, **When** invoca la CLI con `212 f c`, **Then** la CLI responde con `100.00 C` y código de salida 0.
3. **Given** un usuario que requiere convertir 0 °C a Kelvin, **When** invoca la CLI con `0 c k`, **Then** la CLI responde con `273.15 K` y código de salida 0.
4. **Given** un usuario que requiere convertir 373.15 K a Celsius, **When** invoca la CLI con `373.15 k c`, **Then** la CLI responde con `100.00 C` y código de salida 0.
5. **Given** un usuario que requiere convertir 32 °F a Kelvin, **When** invoca la CLI con `32 f k`, **Then** la CLI responde con `273.15 K` y código de salida 0.
6. **Given** un usuario que requiere convertir 273.15 K a Fahrenheit, **When** invoca la CLI con `273.15 k f`, **Then** la CLI responde con `32.00 F` y código de salida 0.
7. **Given** un usuario que introduce la misma unidad de origen y destino (e.g. `25 C C`), **When** ejecuta la conversión, **Then** la CLI preserva el valor numérico formateado a dos decimales (`25.00 C`) con código de salida 0.
8. **Given** una temperatura negativa físicamente válida (e.g. -40 °C), **When** el usuario ejecuta `-40 C F`, **Then** la CLI devuelve `-40.00 F` con código de salida 0.

---

### User Story 2 - Validación de Límites Físicos y Cero Absoluto (Priority: P2)

Como usuario o sistema automatizado, deseo que la CLI rechace cualquier temperatura que viole el límite termodinámico del cero absoluto en la escala de origen, para evitar cálculos físicos imposibles y garantizar la veracidad de los datos.

**Why this priority**: Garantiza la integridad física y científica de las operaciones antes de proceder con cualquier transformación matemática.

**Independent Test**: Puede probarse de manera independiente ingresando valores inferiores a los límites del cero absoluto (-273.15 C, -459.67 F y 0 K) y verificando que la CLI emite un mensaje descriptivo en stderr y termina con código de salida 2, mientras que los valores iguales al cero absoluto se procesan con éxito.

**Acceptance Scenarios**:

1. **Given** un valor en Celsius estrictamente inferior al cero absoluto (`-273.16 C F`), **When** se ejecuta la CLI, **Then** el sistema emite un mensaje de error legible en stderr indicando que el valor está por debajo del cero absoluto (-273.15 C) y finaliza con código de salida 2.
2. **Given** un valor en Fahrenheit estrictamente inferior al cero absoluto (`-459.68 F C`), **When** se ejecuta la CLI, **Then** el sistema emite un mensaje de error legible en stderr indicando la violación del cero absoluto (-459.67 F) y finaliza con código de salida 2.
3. **Given** un valor en Kelvin negativo (`-0.01 K C` o `-5 K F`), **When** se ejecuta la CLI, **Then** el sistema emite un mensaje de error legible en stderr indicando que Kelvin no admite valores negativos (< 0 K) y finaliza con código de salida 2.
4. **Given** el valor exacto del cero absoluto (`-273.15 C K`, `-459.67 F K`, o `0 K C`), **When** se ejecuta la CLI, **Then** el sistema acepta el valor, genera la conversión precisa (`0.00 K` o `-273.15 C`) y finaliza con código de salida 0.

---

### User Story 3 - Manejo Robusto de Entradas No Numéricas, Especiales y Extremas (Priority: P3)

Como operador de línea de comandos, deseo recibir mensajes de diagnóstico claros y códigos de salida predecibles ante entradas incompletas, caracteres no numéricos, valores literales de coma flotante no deseados (NaN/Infinity) o magnitudes y longitudes desmedidas, para integrar la herramienta de forma segura en scripts y tuberías sin fallos silenciosos ni caídas inesperadas.

**Why this priority**: Brinda resiliencia operacional, protegiendo al sistema frente a abusos de memoria, estados indefinidos y errores de invocación de usuario.

**Independent Test**: Puede probarse invocando la CLI sin argumentos, con cadenas vacías, valores alfanuméricos, literales ("nan", "infinity"), cadenas que excedan 32 caracteres y magnitudes superiores a 1.0e12, comprobando que en todos los casos se retorna código de salida 2 con mensaje claro en stderr.

**Acceptance Scenarios**:

1. **Given** una invocación sin argumentos o con argumentos vacíos (e.g. `"" C F`), **When** se ejecuta el comando, **Then** la CLI muestra un mensaje de uso y error en stderr y finaliza con código de salida 2.
2. **Given** un valor no numérico (e.g. `abc C F` o `12.3.4 K C`), **When** se procesa la entrada, **Then** la CLI emite un mensaje en stderr indicando que el valor no es un número válido y finaliza con código de salida 2.
3. **Given** cadenas que representan literales especiales de punto flotante en cualquier combinación de mayúsculas/minúsculas (e.g. `NaN`, `nan`, `Infinity`, `inf`, `+inf`, `-inf`, `-Infinity`), **When** se introducen como valor numérico, **Then** la CLI las rechaza explícitamente como entradas numéricas inválidas con mensaje en stderr y código de salida 2.
4. **Given** una cadena de valor numérico con longitud excesiva superior a 32 caracteres, **When** se recibe como argumento, **Then** la CLI rechaza la entrada por longitud excesiva con mensaje en stderr y finaliza con código de salida 2.
5. **Given** un número con magnitud excesiva superior en valor absoluto a 1.0e12 (e.g. `1e13 C F`), **When** se valida la entrada, **Then** la CLI rechaza el valor por exceder el rango admisible con mensaje en stderr y finaliza con código de salida 2.
6. **Given** una unidad no reconocida (distinta de C, F, K en mayúsculas o minúsculas, e.g. `100 X C`), **When** se analiza el argumento, **Then** la CLI emite un mensaje indicando que las unidades permitidas son C, F o K y finaliza con código de salida 2.

---

### Edge Cases

- **Cero con signo negativo**: Un valor de entrada de `-0` o `-0.0` en cualquier escala válida no debe mostrarse como `-0.00`, sino normalizarse a `0.00 <UNIDAD>`.
- **Límites de precisión y redondeo**: Valores con más de dos decimales (como `25.555`) deben redondearse estrictamente a dos posiciones decimales (`25.56`) siguiendo el redondeo aritmético convencional.
- **Espacios en blanco circundantes**: Cadenas de entrada con espacios iniciales o finales (e.g. `" 100 "`, `" c "`, `" f "`) deben sanearse y aceptarse si el contenido interior es válido.
- **Notación científica moderada**: Representaciones exponenciales estándar como `1e2` o `2.5e1` que cumplan los límites de longitud (<= 32 caracteres) y magnitud (|T| <= 1.0e12) se procesan correctamente evaluando su valor numérico real (`100.00`, `25.00`).
- **Punto de corte exacto de cero absoluto en Fahrenheit**: `-459.67` °F corresponde exactamente a `0.00 K` y `-273.15 C`. Cualquier valor matemáticamente inferior a `-459.67` (como `-459.671`) debe ser rechazado.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La CLI DEBE recibir como argumentos de entrada: el valor numérico de la temperatura, la unidad de escala de origen y la unidad de escala de destino.
- **FR-002**: El sistema DEBE aceptar las unidades de escala 'C', 'F' y 'K' de forma insensible a mayúsculas y minúsculas ('c', 'C', 'f', 'F', 'k', 'K').
- **FR-003**: El sistema DEBE realizar conversiones correctas y bidireccionales entre todos los pares de escalas: Celsius ↔ Fahrenheit, Celsius ↔ Kelvin, y Fahrenheit ↔ Kelvin.
- **FR-004**: El sistema DEBE preservar el valor numérico de la temperatura cuando la unidad de origen y la unidad de destino sean idénticas.
- **FR-005**: El sistema DEBE aceptar valores negativos siempre y cuando sean físicamente válidos (iguales o superiores al cero absoluto en la escala de origen).
- **FR-006**: El sistema DEBE rechazar cualquier valor de temperatura estrictamente inferior al cero absoluto (-273.15 °C, -459.67 °F, 0 K) en la unidad de origen, emitiendo un mensaje de error legible en la salida de error estándar (stderr) y finalizando con código de salida 2.
- **FR-007**: El sistema DEBE aceptar los valores exactos en el umbral del cero absoluto (-273.15 en Celsius, -459.67 en Fahrenheit y 0 en Kelvin) como válidos para su procesamiento y conversión.
- **FR-008**: El sistema DEBE presentar el resultado de una conversión exitosa en la salida estándar (stdout) formateado exactamente a dos lugares decimales, seguido de un espacio y el símbolo de la unidad destino en mayúscula (e.g. `212.00 F`, `0.00 K`), finalizando con código de salida 0.
- **FR-009**: El sistema DEBE validar que la entrada numérica sea un número decimal finito válido, rechazando entradas vacías, argumentos faltantes o cadenas con caracteres no numéricos con un mensaje legible en stderr y código de salida 2.
- **FR-010**: El sistema DEBE rechazar explícitamente los literales especiales de punto flotante ("NaN", "nan", "Infinity", "inf", "+inf", "-inf", "-Infinity") tratándolos como valores no numéricos inválidos, emitiendo un mensaje en stderr y finalizando con código de salida 2.
- **FR-011**: El sistema DEBE limitar la longitud de la cadena del valor numérico a un máximo de 32 caracteres, rechazando cadenas más largas con un mensaje de error en stderr y finalizando con código de salida 2.
- **FR-012**: El sistema DEBE rechazar valores numéricos cuya magnitud absoluta sea estrictamente superior a 1.0e12 con un mensaje de error en stderr y código de salida 2.
- **FR-013**: El sistema DEBE validar que las unidades de origen y destino pertenezcan exclusivamente al conjunto {C, F, K}, rechazando cualquier otra unidad con un mensaje en stderr y código de salida 2.

### Key Entities *(include if feature involves data)*

- **Lectura de Temperatura**: Representa el dato de entrada o salida, compuesto por una magnitud numérica finita y una unidad de escala térmica asociada.
- **Escala de Temperatura**: Define los sistemas de medición soportados (Celsius, Fahrenheit, Kelvin), sus símbolos normalizados y sus correspondientes límites físicos de cero absoluto.
- **Operación de Conversión**: Representa la transformación matemática aplicada entre una escala origen y una escala destino, garantizando la conservación del estado físico y el formateo estricto a dos decimales.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de las conversiones válidas entre Celsius, Fahrenheit y Kelvin producen resultados matemáticamente correctos y formateados a exactamente dos posiciones decimales con su unidad destino en mayúscula.
- **SC-002**: El 100% de las invocaciones con valores inferiores al cero absoluto son rechazadas informando la razón física del rechazo y concluyendo con código de salida 2.
- **SC-003**: El 100% de las invocaciones erróneas (argumentos faltantes, valores no numéricos, NaN, infinitos, unidades desconocidas, longitud > 32 caracteres, magnitud > 1.0e12) finalizan con código de salida 2 y mensaje descriptivo en stderr sin producir excepciones no controladas ni trazas técnicas de depuración.
- **SC-004**: El tiempo de ejecución en frío de la herramienta CLI para cualquier consulta es inferior a 200 milisegundos en el entorno local.

## Assumptions

- La invocación se realiza mediante una interfaz de línea de comandos estándar recibiendo los parámetros en el orden `<valor> <unidad_origen> <unidad_destino>`.
- La salida para casos exitosos se canaliza únicamente por stdout y los errores por stderr.
- El formateo a dos decimales aplica reglas matemáticas estándar de redondeo al decimal más próximo.
- El entorno de ejecución provee un entorno estándar con soporte para la biblioteca estándar del lenguaje sin requerir conectividad de red ni almacenamiento persistente.
