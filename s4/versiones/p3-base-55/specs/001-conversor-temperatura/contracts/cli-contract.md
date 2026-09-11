# CLI Interface Contract: Conversor de Temperatura

**Feature**: [spec.md](../spec.md)
**Module**: `temperatura.cli` / `python -m temperatura`
**Date**: 2026-09-10
**Status**: Finalized

Define la interfaz de línea de comandos, validación posicional, flujos de salida estándar, flujos de error y códigos de salida del sistema.

---

## 1. Esquema de Invocación

```text
python -m temperatura <valor> <unidad_origen> <unidad_destino>
```

O mediante el gestor del proyecto:
```text
uv run python -m temperatura <valor> <unidad_origen> <unidad_destino>
```

---

## 2. Argumentos Posicionales

| Posición | Nombre | Tipo | Restricciones / Reglas |
|---|---|---|---|
| `1` | `<valor>` | String | • Obligatorio.<br>• Longitud máxima: 32 caracteres (evaluada antes de procesar).<br>• Debe representar un número finito (formato decimal estándar o notación científica como `-1e2`, `2.5e1`).<br>• Prohibidos literales especiales: `nan`, `NaN`, `inf`, `Infinity`, `+inf`, `-inf`, etc.<br>• Magnitud absoluta acotada: $\|T\| \le 1.0 \times 10^{12}$.<br>• Límite físico: debe ser mayor o igual al cero absoluto de la unidad origen. |
| `2` | `<unidad_origen>` | String | • Obligatorio.<br>• Insensible a mayúsculas/minúsculas.<br>• Valores aceptados: `C`, `c`, `F`, `f`, `K`, `k`. |
| `3` | `<unidad_destino>` | String | • Obligatorio.<br>• Insensible a mayúsculas/minúsculas.<br>• Valores aceptados: `C`, `c`, `F`, `f`, `K`, `k`. |

---

## 3. Protocolo de Flujos de E/S y Códigos de Salida

### 3.1 Salida Exitosa (`stdout`)
- **Código de salida**: `0`
- **Flujo**: `sys.stdout`
- **Formato**: `<VALOR_CON_DOS_DECIMALES> <UNIDAD_DESTINO_MAYUSCULA>\n`
- **Ejemplos**:
  - `100.00 C`
  - `212.00 F`
  - `273.15 K`
  - `0.00 K`
  - `-40.00 F`

### 3.2 Salida de Error (`stderr`)
- **Código de salida**: `2`
- **Flujo**: `sys.stderr`
- **Formato**: Mensaje explicativo legible en texto plano terminado en salto de línea, sin trazas de excepciones (`Traceback`) ni volcados internos.
- **Ejemplos**:
  - `Error: Se requieren exactamente 3 argumentos: <valor> <unidad_origen> <unidad_destino>`
  - `Error: La longitud del valor numérico excede el límite permitido de 32 caracteres.`
  - `Error: El valor 'abc' no es un número válido.`
  - `Error: Los valores literales 'nan' e 'inf' no están permitidos.`
  - `Error: El valor '1e13' excede la magnitud máxima permitida (1e12).`
  - `Error: Unidad 'X' no válida. Use C, F o K.`
  - `Error: La temperatura -300.00 C está por debajo del cero absoluto (-273.15 C).`

---

## 4. Matriz de Casos de Validación y Contrato

| Escenario | Comando | Stdout | Stderr | Exit Code |
|---|---|---|---|:---:|
| Conversión C ➔ F | `python -m temperatura 100 C F` | `212.00 F` | *(vacío)* | `0` |
| Conversión F ➔ C | `python -m temperatura 212 f c` | `100.00 C` | *(vacío)* | `0` |
| Conversión C ➔ K | `python -m temperatura 0 C K` | `273.15 K` | *(vacío)* | `0` |
| Conversión K ➔ C | `python -m temperatura 373.15 k c` | `100.00 C` | *(vacío)* | `0` |
| Preservación misma unidad | `python -m temperatura 25 C C` | `25.00 C` | *(vacío)* | `0` |
| Negativo válido C ➔ F | `python -m temperatura -40 C F` | `-40.00 F` | *(vacío)* | `0` |
| Notación científica válida | `python -m temperatura -1e2 C K` | `173.15 K` | *(vacío)* | `0` |
| Cero absoluto exacto K ➔ C | `python -m temperatura 0 K C` | `-273.15 C` | *(vacío)* | `0` |
| Cero absoluto exacto C ➔ K | `python -m temperatura -273.15 C K` | `0.00 K` | *(vacío)* | `0` |
| Normalización de cero negativo | `python -m temperatura -0.001 C C` | `0.00 C` | *(vacío)* | `0` |
| Bajo cero absoluto en C | `python -m temperatura -273.16 C F` | *(vacío)* | `Error: ... cero absoluto ...` | `2` |
| Bajo cero absoluto en F | `python -m temperatura -459.68 F C` | *(vacío)* | `Error: ... cero absoluto ...` | `2` |
| Bajo cero absoluto en K | `python -m temperatura -1 K C` | *(vacío)* | `Error: ... cero absoluto ...` | `2` |
| Entrada no numérica | `python -m temperatura abc C F` | *(vacío)* | `Error: ... no es un número válido ...` | `2` |
| Entrada NaN | `python -m temperatura nan C F` | *(vacío)* | `Error: ... no están permitidos ...` | `2` |
| Entrada Infinito | `python -m temperatura Infinity C F` | *(vacío)* | `Error: ... no están permitidos ...` | `2` |
| Cadena > 32 caracteres | `python -m temperatura 123456789012345678901234567890123 C F` | *(vacío)* | `Error: ... excede el límite ...` | `2` |
| Magnitud > 1e12 | `python -m temperatura 1e13 C F` | *(vacío)* | `Error: ... magnitud máxima ...` | `2` |
| Unidad no soportada | `python -m temperatura 100 X F` | *(vacío)* | `Error: ... Unidad 'X' no válida ...` | `2` |
| Argumentos insuficientes | `python -m temperatura 100 C` | *(vacío)* | `Error: Se requieren exactamente 3 ...` | `2` |
