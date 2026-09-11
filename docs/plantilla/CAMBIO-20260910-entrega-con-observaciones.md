# Estado de entrega con observaciones

Fecha: 2026-09-10. Alcance: generador de informes y contrato de datos; sin cambios en entradas, informes, evidencias ni publicación.

Se añadió `entrega_con_observaciones` para que P1 pueda registrar un 429 no observado en ensayos reales acotados sin declarar cumplido ese requisito. Solo permite `manejo_429` pendiente, con observación `no_observado`, evidencia `ensayo_sin_429` y textos de protocolo, resultado y límite. Conserva todas las guardias de evidencia verificada, fuente legible, integridad, ausencia de simulaciones, revisión de autoría y contenido, y repositorio accesible.

El PDF y el DOCX incluyen el aviso del estado y la observación completa. El resultado de validación y el manifiesto declaran `cumplimiento_total: false` y el único requisito pendiente. El modo `final` conserva la obligación de demostrar un 429 real; el nuevo estado no certifica cumplimiento total ni aceptación académica.

## Verificación

Comando reproducible desde la raíz del proyecto, con Python documental que incluya las dependencias del generador:

```bash
python docs/plantilla/test_guardias_reportes.py
```

Resultado: **27 pruebas aprobadas**. Incluyen el caso positivo documentado y rechazos por observación incompleta, fuente ausente, repositorio pendiente o de ejemplo, evidencia simulada o sin verificar, contenido sin revisar, otro requisito pendiente, requisito oculto o declarado cumplido, respaldo obligatorio ausente, contradicción con una evidencia `manejo_429`, uso fuera de P1 e intento de relajar `final`.

Las pruebas de composición verifican que el aviso y los textos de la observación llegan a ambos formatos. Usan documentos en memoria y dobles de las operaciones de imagen, escritura y generación; las entradas son fixtures identificadas explícitamente como ficticias. Las pruebas del manifiesto comprueban el estado de cumplimiento incompleto. No son evidencia de ejecución académica.

No se generaron PDFs ni DOCX, ni se modificaron artefactos previos para esta verificación. La inspección visual de páginas queda a cargo de la generación posterior con la entrada y las evidencias reales revisadas. La estructura validada y los hashes no certifican la autenticidad o la suficiencia semántica de un registro.

## Reversibilidad

Cambio acotado al generador, su contrato y sus pruebas. Las salidas continúan exigiendo una carpeta nueva y creación exclusiva. No se ejecutaron eliminaciones, sobrescrituras de informes ni commits.
