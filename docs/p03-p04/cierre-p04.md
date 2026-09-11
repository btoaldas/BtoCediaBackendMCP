# Cierre técnico de la práctica 4

## Resultado y alcance

La base canónica `s4/mi-proyecto-speckit/` contiene el conversor corregido,
65 pruebas: 23 unitarias, 31 de integración en memoria y 11 e2e por subprocess.
La cobertura medida es 116/123 líneas (94,3%). Una instalación nueva con
`uv sync --frozen` y la suite completa aprobó otra vez; una revisión independiente
comprobó 17 procesos CLI y el umbral con un oráculo racional Fraction.
No hay hallazgos pendientes en las tres categorías de la revisión de laboratorio.

P3 permanece reproducible como etapa histórica en `s4/versiones/p3-base-55/`.
No se le atribuyen los 10 tests añadidos en P4 ni se cambian sus fuentes históricas.
El escenario B conserva su versión de 60 pruebas previa al segundo fix numérico;
E parte de 65. Ambos tienen manifiestos de origen. Los fallos intencionales
viven en snapshots de evidencia, no en la versión canónica recomendada.

## Ejecución real y autoría

- Spec Kit creó la especificación, plan y tareas mediante los comandos reales
  ejecutados en agy. No se escribió un test-spec.md alternativo para P4.
- Codex preparó los siete skills, tres archivos de agente, scripts y hook a partir
  de la guía, con ajustes deterministas documentados. La configuración de higiene
  ya estaba presente cuando security-agent la verificó.
- A utilizó el tester nativo; revisiones adicionales encontraron Overflow y doble
  redondeo que la primera suite verde no detectaba. agy añadió regresiones y
  corrigió `copy_abs` y la precisión local 80, conservando RED y GREEN.
- En B, agy introdujo +32.05 y corrigió +32 tras un Stop auténtico: 9 fallos/51
  aprobados, exit 1, decision=continue; el Stop posterior registró 60 aprobados y {}.
- En E, Codex introdujo ROUND_DOWN en el formato de una copia aislada. Stop
  registró 5 fallos/60 aprobados, y agy restauró ROUND_HALF_UP. El principal
  adaptó los roles nativos mediante DefineSubagent para disponer de ejecución.
- security-agent-native emitió un hallazgo sobre dos except Exception. El
  principal agy restringió las capturas y el security volvió a revisar el código.
  Codex trasladó exactamente ese archivo CLI a la base canónica, con respaldo.
- tester-agent-native produjo JSON nuevos por cada capa: 23/31/11 y total 65;
  report-agent-native ejecutó generar_reporte.py y emitió el HTML E APROBADO.
  Las fuentes y tests finales de E y canónico se compararon byte a byte.

El flujo requirió permisos y una corrección de compatibilidad del runtime. No se
presenta como una sesión sin intervención ni se atribuye al tester la ejecución
que el principal hizo cuando un primer subagente carecía de herramientas.
La pasada por capas con JSON y la generación de HTML fueron invocaciones reales.
Los registros originales privados se conservan; los resúmenes públicos se derivan
con hashes y omiten rutas de usuario y contexto privado.

## Reproducción

Desde `s4/mi-proyecto-speckit/`:

```sh
uv sync --frozen
uv run python -m temperatura 0 C F
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v
uv run pytest tests/e2e/ -v
uv run pytest --cov=src --cov-report=term-missing
uv run python .agents/skills/qa-report/generar_reporte.py
```

Para el flujo nativo abrir `agy` en esa carpeta, confiar únicamente en ella y
usar `/qa-orchestrate`. Su adaptación documentada conserva los roles y activa
la capacidad de ejecución mediante una herramienta nativa cuando es necesaria.
Los permisos se revisan por acción. El hook se carga desde `.agents/hooks.json`
y el comando se resuelve relativo a ese directorio. Una invocación manual del
script sirve como diagnóstico, pero no prueba por sí sola un Stop automático.

## Reflexiones técnicas para revisión del estudiante

Un skill contiene una receta concreta; un agente decide cómo aplicar las recetas
de su rol. Aquí el orden fue pedagógico: tester antes del informe permite incluir
las regresiones; security y report no intercambian mensajes directos, y el
reportador vuelve a ejecutar pruebas, cobertura y el patrón de secretos.

La orquestación evitó elegir el orden a cada paso, pero los permisos y fallos del
runtime mantuvieron intervención humana. La delegación no eliminó el control:
se conservaron fuentes, se revisaron acciones y el Stop exigió corregir las pruebas
fallidas. La configuración declarada no equivale a un aislamiento por skill.

El inspector encontró dos capturas genéricas de excepciones; la verificación
independiente encontró además dos defectos numéricos que una suite verde no
había detectado. El veredicto final es APROBADO bajo el umbral y condiciones del
reportador. Estas son conclusiones técnicas de las evidencias, no respuestas
que finjan sensaciones personales ni una reflexión oral que no se realizó.
