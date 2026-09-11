# Hallazgos de Seguridad

| Caso | Lo que se encontró | Corrección sugerida |
|---|---|---|
| 🔑 Secreto expuesto | Sin hallazgos | Mantener la política de inyección de configuración mediante variables de entorno y no versionar archivos .env. |
| 🧪 Validación de entradas | Sin hallazgos | Mantener las validaciones actuales de tipo (Decimal), formato (rechazo de literales nan/inf y vacíos), longitud (límite de 32 caracteres) y rango (magnitud máxima 1e12 y cero absoluto por escala). |
| 🚪 Manejo de excepciones | Sin hallazgos | Mantener la captura de excepciones específicas (`InvalidOperation`, `ErrorTemperatura`) evitando cláusulas genéricas o silenciamiento de errores. |

## Acciones de higiene aplicadas
Ninguna, ya estaba en orden.
- `.env.example` ya existe con la plantilla informativa del proyecto.
- `.env` se encuentra debidamente ignorado en `.gitignore` (verificado con `git check-ignore -q .env` y `git check-ignore --no-index -q .env`, retorno 0).
- `.env` no se encuentra trackeado en el repositorio Git (verificado con `git ls-files --error-unmatch .env`, retorno 1).
