# Ajustes proporcionados al reportador de la guía

El script original se conserva localmente como
`.agents/skills/qa-report/generar_reporte_guia_original.py` y está excluido del
repositorio público. El ejecutable
`generar_reporte.py` mantiene la misma finalidad y umbral de cobertura (50%),
pero incorpora comprobaciones necesarias para no mostrar un falso APROBADO:

| Condición | Ajuste | Prueba |
|---|---|---|
| pytest termina con error o sin recolección | Exige exit 0 y total > 0, además de fallos y errores = 0 | verificar_reportador.py: sin_tests, pytest_error, error_coleccion |
| Podrían quedar JSON anteriores | Cada corrida usa ruta nueva con fecha UTC y copia su reporte | .qa-runs/<timestamp>/ |
| `.env` todavía no existe | `git check-ignore --no-index -q .env` evalúa reglas reales | env_no_ignorado |
| Un hallazgo contiene HTML | Escape de salida y omisión del valor sensible | hallazgo_html |
| La cobertura queda justo en el umbral | 49.9 rechaza, 50.0 acepta | cobertura_baja, limite_50 |

El autor del script mejorado es Codex. Los resultados de su verificación son
pruebas del reportador, separadas de las pruebas del conversor: no aumentan
artificialmente la cobertura de la aplicación. Se comprobaron once estados.
Las entradas de esa comprobación son estados sintéticos de control, identificados
como tales; las cifras del entregable se obtienen ejecutando pytest realmente.

El patrón de detección de secretos es una revisión básica, no un escáner completo.
La tabla de seguridad incluye revisión adicional de las entradas y excepciones.
No se hace ninguna afirmación de certificación o ausencia universal de riesgos.
