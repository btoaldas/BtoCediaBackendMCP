# Generación de informes del curso

El generador `scripts/reportes_curso.py` crea PDF y DOCX editable a partir de un JSON explícito. No consulta servicios externos, no inventa resultados y no publica entregas. Los originales del docente se conservan en `materiales/`.

## Uso

Ejecutar con el Python del runtime documental que incluye `python-docx`, `reportlab`, `Pillow` y `pypdf`.

```bash
python scripts/reportes_curso.py privado/practica-1.json --validar
python scripts/reportes_curso.py privado/practica-1.json --salida informes/practica-01/version-01
```

La salida debe ser una **carpeta nueva**. El programa reserva la carpeta después de construir ambos documentos en memoria y usa creación exclusiva; no tiene opción de sobrescritura. Deja PDF, DOCX y `manifiesto.json` con hashes de entrada, artefactos, imágenes y fuentes. Ante un error de escritura, conserva cualquier archivo ya generado para inspección.

## Datos de entrada

Las rutas de imágenes y fuentes se resuelven contra la carpeta del JSON. El JSON privado puede contener identificación; el manifiesto registra nombres de archivo y hashes, sin rutas absolutas ni valores de credenciales.

| Campo | Contenido |
|---|---|
| `version` | Entero `1` |
| `estado` | `borrador`, `prueba`, `final` o `entrega_con_observaciones`; predeterminado `borrador` |
| `practica` | `numero` 1–4, `titulo` según guía y `clase` como texto opcional |
| `estudiante.nombre` | Nombre completo real del estudiante |
| `fecha` | ISO `YYYY-MM-DD`; omitida usa fecha actual de America/Guayaquil; no admite futuro |
| `explicacion` | Párrafo o lista de párrafos. Redactar la explicación breve pedida, aproximadamente 3–5 líneas |
| `evidencias` | Lista de evidencias con esquema siguiente |
| `repositorio` | `url` HTTPS y `acceso_docente_verificado` booleano; obligatorio en P1, P3 y P4; opcional en P2 |
| `reflexion` | Texto o lista de párrafos, cuando la guía lo pida |
| `secciones` | Bloques complementarios con párrafos y tablas, según la guía de cada práctica |
| `requisitos` | Lista de `descripcion`, `estado` (`cumplido`, `pendiente`, `no_aplica`), `evidencia_ids` e `id` opcional. En `entrega_con_observaciones` es obligatorio declarar `id: manejo_429` como pendiente según el contrato siguiente |
| `observaciones` | Lista admitida únicamente en `entrega_con_observaciones`, con una observación documentada de P1 según el contrato siguiente |
| `contenido_revisado` | `true` solo después de revisar afirmaciones y autoría; obligatorio en `final` y `entrega_con_observaciones` |

Cada evidencia necesita:

```json
{
  "id": "conversacion_8_turnos",
  "titulo": "Recuerdo del primer turno en el octavo",
  "tipo": "captura",
  "imagen": "capturas/conversacion.png",
  "fuente": "capturas/conversacion.png",
  "descripcion": "Descripción precisa de lo que demuestra la captura real.",
  "verificada": true
}
```

`tipo` admite `captura`, `registro_renderizado` o `simulacion`. Un registro renderizado conserva el log original como `fuente` y aparece explícitamente como **Registro de ejecución**, sin presentarse como captura de una UI. Para una captura de pantalla original, `fuente` puede ser la misma imagen. `sha256_imagen` y `sha256_fuente` son opcionales; si se proporcionan, se exige coincidencia. `verificada` declara revisión humana/agente contra la ejecución original; el programa no puede certificar autenticidad a partir de un PNG.

No añadir secretos, claves API, cookies, datos de terceros o rutas privadas a imágenes ni registros. Las fuentes referenciadas deben sanearse antes de producir el informe; el generador no redacta imágenes automáticamente.

## Secciones y tablas

```json
{
  "titulo": "Comparación de las ejecuciones",
  "posicion": "antes_evidencia",
  "parrafos": ["Interpretación apoyada en las salidas originales."],
  "tabla": {
    "columnas": ["Versión", "Cambio", "Resultado observado"],
    "anchos": [1, 2, 3],
    "filas": [["A", "Texto del cambio aplicado", "Resultado comprobado"]]
  }
}
```

`posicion` admite `antes_evidencia` y `despues_evidencia` (predeterminada). Los anchos son pesos relativos positivos. Máximo seis columnas, con encabezado repetido al continuar página. `parrafos` puede quedar vacío si el bloque es solamente una tabla. No se exige una reflexión inventada: el responsable aporta la reflexión real solicitada por la guía.

## Estados y cierre

`borrador` admite pendientes y los identifica visiblemente. `prueba` muestra **PRUEBA TÉCNICA DEL GENERADOR - NO ENTREGAR** y debe guardarse en `.tmp/`. El ejemplo incluido es deliberadamente incompleto y no sirve como entrega.

`final` exige evidencia verificada, ningún tipo `simulacion`, contenido revisado y ningún requisito declarado pendiente. La obligatoriedad del repositorio y el contenido mínimo dependen del entregable de cada guía:

| Práctica | Repositorio | Evidencias por ID | Contenido adicional obligatorio del informe |
|---|---|---|---|
| 1 | Sí, URL HTTPS y acceso docente verificado | `conversacion_8_turnos`, `manejo_429`, `repositorio` | Explicación breve de implementación y estrategia de memoria |
| 2 | No | Al menos dos de `ronda_1`, `ronda_2`, `ronda_3`, más `cierre` | Exactamente tres párrafos en `reflexion`, uno por respuesta pedida |
| 3 | Sí, URL HTTPS y acceso docente verificado | `spec_manual`, `flujo_speckit` | Al menos una tabla comparativa en `secciones[].tabla`, más explicación breve |
| 4 | Sí, URL HTTPS y acceso docente verificado | `hook_bloqueando`, `reporte_qa` | Explicación breve de la arquitectura skills y agentes |

La guía P2 dice expresamente que no hace falta repositorio y que se entrega reflexión y capturas. Si P2 omite `repositorio` o deja su URL vacía, PDF y DOCX omiten toda la sección de repositorio: no muestran una publicación pendiente. Si voluntariamente se añade una URL en P2, debe ser válida y tener acceso docente verificado para el estado final.

Las evidencias de las rondas de P2 deben mostrar predicción previa y resultado real; `cierre` debe demostrar el pedido y su resultado. Las tres reflexiones deben responder a las preguntas de la guía sin atribuir al estudiante experiencias o comparaciones que no ocurrieron. Para P3, la tabla debe comparar las dos versiones y sus pruebas; P4 debe mostrar el bloqueo real del hook y el informe QA. El generador comprueba presencia y estructura, pero la suficiencia semántica y la autenticidad requieren revisión contra los registros originales. No basta con asignar el ID esperado a una imagen.

Estas reglas se contrastaron con `materiales/practica_01.md` y la plantilla PDF; `materiales/practica-02.md`, apartado Entregable de la sesión; `materiales/practica-03.md`, apartado Entregable de la sesión; y `materiales/practica-04.md`, apartado Entregable de la sesión. No se exige reflexión escrita en el PDF de P3/P4 cuando el entregable literal no la pide. El código, repositorio, permisos y otras obligaciones de las guías deben seguir verificándose mediante la matriz de cumplimiento; el generador no puede certificarlos por sí solo.

### Entrega con observación de un 429 no observado

`entrega_con_observaciones` está habilitado exclusivamente para P1. Permite documentar un experimento real concluido cuyo resultado fue no observar un error 429 dentro del protocolo ejecutado. **No acredita el manejo de un 429 real, no declara cumplimiento total y no convierte el requisito en cumplido.** La aceptación académica corresponde al docente.

Conserva las exigencias de `final` sobre evidencia real verificada, ausencia de simulaciones, revisión de contenido y autoría, URL HTTPS y acceso docente verificado. Siguen siendo obligatorias las evidencias `conversacion_8_turnos` y `repositorio`. La única evidencia exigida que puede faltar es `manejo_429`; en su lugar deben existir la evidencia `ensayo_sin_429`, con imagen y fuente original legibles, y una observación explícita de tipo `no_observado`. No se admite a la vez una evidencia con ID `manejo_429`, porque contradiría esa observación.

La observación necesita `protocolo`, `resultado` y `limite` como textos no vacíos. El protocolo debe describir los ensayos realmente ejecutados, sus condiciones y límites; el resultado debe ajustarse a sus registros, y el límite debe explicar lo que no se pudo demostrar. No basta con cambiar el nombre de un registro simulado. El generador valida la estructura y la integridad; la persona que marca `contenido_revisado` debe contrastar las afirmaciones con las fuentes.

Fragmento esquemático del contrato; sustituir las instrucciones entre corchetes por hechos comprobados antes de usarlo en una entrada real:

```json
{
  "estado": "entrega_con_observaciones",
  "observaciones": [{
    "requisito_id": "manejo_429",
    "tipo": "no_observado",
    "evidencia_ids": ["ensayo_sin_429"],
    "protocolo": "[Describir los ensayos reales, condiciones y límites ejecutados.]",
    "resultado": "[Describir el resultado observado y enlazado al registro original.]",
    "limite": "[Explicar por qué el resultado no acredita observar y manejar un 429 real.]"
  }],
  "requisitos": [{
    "id": "manejo_429",
    "descripcion": "Observación y manejo de un error 429 real del proveedor",
    "estado": "pendiente",
    "evidencia_ids": ["ensayo_sin_429"]
  }]
}
```

Debe existir exactamente una observación y exactamente un requisito con ID `manejo_429`, declarado `pendiente` y vinculado a todas las evidencias citadas por la observación. No se admite ningún otro requisito pendiente. Todas las referencias deben resolver a evidencias incluidas; `ensayo_sin_429` es obligatorio y pueden añadirse otras fuentes reales como evidencias separadas. El resto de los datos y evidencias de P1 se aporta con el esquema habitual.

PDF y DOCX muestran **INFORME DE ENTREGA CON OBSERVACIONES**, una sección **Observación documentada**, el requisito pendiente, protocolo, resultado, límite y los IDs de respaldo. `--validar` y el manifiesto registran `cumplimiento_total: false` y `requisitos_pendientes: ["manejo_429"]`; el manifiesto conserva también la observación. `ok: true` indica que la entrada satisface este contrato documental, no que se hayan cumplido todos los requisitos académicos.

El estado `final` permanece estricto: sigue exigiendo `manejo_429` y no permite observaciones ni requisitos pendientes. `borrador` y `prueba` conservan su uso previo; las observaciones de este esquema se reservan al nuevo estado.

Antes de entrega: renderizar el DOCX con `render_docx.py` del skill documental y LibreOffice **bundled**, nunca el LibreOffice desktop del usuario. Renderizar PDF con Poppler bundled; inspeccionar todas las páginas de ambos formatos. Revisar texto, orden, número de imágenes, tabla y enlace. Los hashes prueban integridad, no ejecución, acceso al repositorio ni recepción en AVAC.

## Reversibilidad

Toda corrección produce una nueva carpeta de salida. Se preservan plantilla, entradas, registros y versiones previas. El generador no elimina ni revierte archivos.
