# Spec manual — Conversor de temperatura

## Objetivo
Convertir una temperatura entre Celsius, Fahrenheit y Kelvin desde una terminal.

## Criterios de aceptación
- [ ] Convierte C↔F: 0 C = 32 F y 212 F = 100 C.
- [ ] Convierte C↔K: 0 C = 273.15 K y 273.15 K = 0 C; F↔K compone estas fórmulas.
- [ ] Presenta el resultado con exactamente dos decimales y la unidad de destino.
- [ ] Rechaza temperaturas por debajo del cero absoluto (-273.15 C, -459.67 F, 0 K).
- [ ] Acepta únicamente las unidades C, F y K sin distinguir mayúsculas/minúsculas.

## Casos borde
- Entrada vacía o no numérica: mensaje de error legible y código de salida 2.
- Conversión a la misma unidad: conserva el valor y presenta dos decimales.
- Valor exactamente en el cero absoluto: es válido; un valor menor se rechaza.
- Temperaturas negativas por encima del cero absoluto: se convierten normalmente.
