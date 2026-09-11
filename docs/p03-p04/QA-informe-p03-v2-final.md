# Revisión del informe final P3 versión 2

Fecha: 2026-09-10. Resultado: **final documental**, listo para entrega; esta revisión no acredita recepción en AVAC ni aceptación académica.

Entrada nueva: `privado/p03-informe-datos-v4-final.json`, derivada de v3. Salida nueva: `informes/practica-03/version-02-final/`. PDF y DOCX editable tienen seis páginas Letter cada uno. La versión 1, sus entradas, capturas y registros se conservaron; se verificó que los hashes de ambos artefactos anteriores siguen iguales.

## Publicación comprobada

El 10/09/2026 a las 21:26:09 de Ecuador se verificó el repositorio público `https://github.com/btoaldas/BtoCediaBackendMCP` mediante `git ls-remote` y una consulta HTTPS anónima a la API de GitHub. HEAD y main coincidieron en `e455a5dc2acdf4d745a1cf1d66d08794f9c8b347`; se comprobó que el commit base `140f59af38bd654c5e6727b6ff832fae6ff921fd` es ancestro.

Los README se descargaron mediante HTTPS sin cookies, tokens, cabecera Authorization, .netrc ni perfiles de navegador. Respondieron HTTP 200 y sus bytes coincidieron con `git show` del commit publicado:

| Archivo | SHA-256 |
|---|---|
| `s4/clase-sdd/README.md` | `e9a9c50affe7809bee257a85460719663fee2dd846d3051342011f5a06f6e4a5` |
| `s4/versiones/p3-base-55/README.md` | `73ae4869ac5a4689395f36ba427ab48e77f7671da6d8232e160478e1c147be1f` |

El registro completo quedó en `evidencia/repositorio/publicacion-p03-20260910.json`. El PNG homónimo es una representación tipográfica determinista de esas consultas reales, identificada como **registro renderizado**, no captura de UI. El acceso anónimo demuestra disponibilidad para cualquier lector, incluido el docente; no demuestra que el docente haya visitado o aceptado el trabajo.

## Cambio documental y fidelidad

Se añadió la evidencia `repositorio`, se marcó ese requisito como cumplido y se sustituyó el párrafo de publicación pendiente por la ubicación de la versión manual y la base histórica P3. Se mantienen la clase 4, las 55 pruebas históricas (19 unitarias, 27 de integración, 9 e2e), las 19 comprobaciones manuales independientes, las tres comparaciones y la cobertura de 108/122 líneas (88,52 %, redondeada a 89 % por la salida).

El informe conserva la distinción entre análisis técnico asistido y vivencias personales del estudiante; también conserva la diferencia de precisión entre los pedidos de cada bloque. La base `s4/versiones/p3-base-55` reproduce la etapa P3 y declara limitaciones corregidas posteriormente en P4. No se incorporaron conteos de P4 ni se presentó el snapshot histórico como versión corregida.

## Revisión visual y verificación independiente

Se usó el generador existente, Poppler bundled para el PDF y `render_docx.py` con LibreOffice headless bundled para el DOCX. No se usó CUA, navegador ni aplicación de escritorio. No se repitió el marcador global de autoría ni se modificó el generador.

Se inspeccionaron las seis páginas finales de cada formato, doce en total, a 120 dpi:

| Página | Contenido revisado | Resultado en ambos formatos |
|---|---|---|
| 1 | Identificación, clase, explicación y comparación | Tabla y texto completos; sin aviso de borrador |
| 2 | Tres entradas idénticas y registro manual | Encabezado junto a tabla; comandos y resultados legibles |
| 3 | Captura original del visor manual | Imagen completa y sin retoques; detalle legible en página 2 |
| 4 | Registro del flujo y suite P3 | Cuatro comandos, conteos y fallo/corrección de empaquetado legibles |
| 5 | Captura original del visor Spec Kit | Imagen completa y sin retoques; detalle legible en página 4 |
| 6 | Registro de publicación, conclusión y enlace | Commit, README, fecha y hashes legibles; enlace completo |

No se observaron recortes, superposiciones, glifos defectuosos ni títulos huérfanos. Las capturas aportan contexto global a escala menor; los registros separados permiten leer el detalle. Se preservaron espacios de las páginas dedicadas a una figura para no dividirla ni reducir su letra.

El validador devolvió `ok: true`, `estado: final`, cinco evidencias y ningún requisito pendiente. La auditoría comprobó hashes de entrada, fuentes, imágenes y artefactos; las cinco imágenes incrustadas en el DOCX coinciden byte a byte con sus PNG de origen y hay dos tablas editables. La extracción de texto comprobó clase, conteos, cobertura, entradas comparadas, base histórica, commit y URL; no hay aviso de borrador ni rutas privadas. Las doce páginas finales coinciden píxel a píxel con la composición candidata correspondiente.

La evidencia reproducible está en `.tmp/qa-informes/p03-v2-auditoria-final.json`, generada por `.tmp/qa-informes/p03-v2-auditar.py`. Los renderizados finales están en `.tmp/qa-informes/p03-v2-pdf-final/` y `.tmp/qa-informes/p03-v2-docx-final/`. El script `.tmp/qa-informes/p03-v2-preparar.py` conserva el método de consulta anónima y la construcción determinista del registro; usa salidas exclusivas y no debe ejecutarse sobre nombres ya existentes.

| Artefacto | Bytes | SHA-256 |
|---|---:|---|
| `Informe-Practica-03.pdf` | 1293479 | `ffbbc6d338c3f2bd95fd1da71d4e369fe94b05fcfb2bf42fe5bb22502f05a72b` |
| `Informe-Practica-03.docx` | 1497222 | `67c64c9b762a84bfc72f4a372988d2877705125db6a2b7064e900cdb8b64cecc` |

Los renderizadores terminaron con código 0. Poppler emitió los avisos conocidos de Fontconfig; no se modificó la configuración/caché y la revisión visual no detectó pérdida de texto. No se hicieron commits ni cambios en fuentes de P4.
