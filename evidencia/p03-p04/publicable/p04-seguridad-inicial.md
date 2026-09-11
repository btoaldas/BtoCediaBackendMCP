# Hallazgos de Seguridad

| Caso | Lo que se encontró | Corrección sugerida |
|---|---|---|
| 🔑 Secreto expuesto | Sin hallazgos | Mantener la política de inyección de configuración mediante variables de entorno y no versionar archivos .env. |
| 🧪 Validación de entradas | Sin hallazgos | Mantener las validaciones actuales de tipo (Decimal), formato (rechazo de literales nan/inf y vacíos), longitud (límite de 32 caracteres) y rango (magnitud máxima 1e12 y cero absoluto por escala). |
| 🚪 Manejo de excepciones | En `src/temperatura/cli.py` se identificó el uso de `except Exception` genérico: línea 41 `except (InvalidOperation, Exception):` y línea 64 `except Exception as err:`. | Restringir la captura en la conversión numérica a `InvalidOperation` (`from decimal import InvalidOperation`). En el bloque final, capturar excepciones específicas del dominio o registrar la traza antes de finalizar para no enmascarar errores no anticipados. |

## Acciones de higiene aplicadas
Ninguna, ya estaba en orden.
- `.env.example` ya existe con la plantilla informativa del proyecto.
- `.env` se encuentra debidamente ignorado en `.gitignore` (verificado con `git check-ignore --no-index -q .env`, retorno 0).
- `.env` no se encuentra trackeado en el repositorio Git (verificado con `git ls-files --error-unmatch .env`, retorno 1).
