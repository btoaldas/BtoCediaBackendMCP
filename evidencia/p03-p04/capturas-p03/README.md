# Evidencia conservada de P3

Este paquete reúne registros, visores HTML y dos capturas PNG reales de esos
visores. No representa una terminal original, una nueva ejecución, asistencia a
clase ni aceptación del docente. Documenta la base histórica de **55 pruebas de
P3**, anterior a las ampliaciones y correcciones numéricas de P4.

## Qué consultar

- [Especificación manual y tres casos](manual-v1.html): resumen fiel de la spec,
  tres comandos, stdout, stderr y códigos de salida conservados.
- [Flujo de Spec Kit](flujo-v1.html): cuatro invocaciones, artefactos, estados
  rojos y verdes, 55 pruebas (19 unitarias, 27 integración, 9 e2e), cobertura
  histórica de 108/122 líneas y fallo de empaquetado descubierto en un entorno
  nuevo, seguido de su corrección.
- [Registro manual legible](registro-manual-v1.txt) y
  [registro completo del flujo](registro-flujo-v1.txt): texto y valores JSON
  utilizados por los visores; se pueden inspeccionar sin navegador.
- [Captura del visor manual](captura-visor-p03-spec-manual-20260910.png) y
  [captura del visor de Spec Kit](captura-visor-p03-flujo-speckit-20260910.png):
  PNG originales, sin edición de píxeles, obtenidos el 10 de septiembre de 2026
  mediante CUA nativa de Microsoft Edge y FireShot.

Los dos HTML son autocontenidos, sin JavaScript ni recursos de red externos.
Se pueden abrir localmente manteniendo los archivos de esta carpeta juntos.
Sus enlaces de navegación y de procedencia resuelven dentro de la carpeta.
Las capturas muestran la vista con el desplegable inferior cerrado; los HTML
permiten expandir la spec original o los argumentos completos.

## Procedencia histórica y resultado vigente

[procedencia-v1.json](procedencia-v1.json) es la fuente congelada de la
**preparación anterior a las capturas**. Los campos `capturas_realizadas: false`,
`navegador_abierto: false` y revisión visual pendiente describen exclusivamente
ese momento. Se conserva sin cambios porque los HTML y los hashes de la
preparación original lo referencian; no es el estado final de las capturas.

El resultado posterior y vigente está en
[procedencia-capturas-v1.json](procedencia-capturas-v1.json): identifica método,
fecha, dimensiones, hashes de los PNG, hashes de sus HTML y comprobación de las
fuentes. [evidencias-pdf-capturas-v1.json](evidencias-pdf-capturas-v1.json)
contiene los IDs `spec_manual` y `flujo_speckit`, marcados como verificados, con
leyendas que los describen como capturas de visores de registros conservados.
Es un fragmento para integrar en un informe, no un informe completo.

La URL de loopback `127.0.0.1:8933` en la procedencia registra dónde se sirvió el
visor al capturarlo. No es un sitio público ni una instrucción de abrir un
servidor actual. `Downloads/FireShot/...` identifica la ubicación relativa de
las copias originales conservadas localmente; no promete acceso público a ellas.

## Fuentes y límites de reproducción

La base exacta utilizada por los visores está en
[p03-resultados-base.json](../publicable/p03-resultados-base.json).
[p03-resultados-base-v2.json](../publicable/p03-resultados-base-v2.json)
conserva los mismos resultados y añade la referencia con hash de la corrida
comparativa. [p03-snapshot-verificado.json](../publicable/p03-snapshot-verificado.json)
registra una comprobación posterior del snapshot: `55 passed in 0.31s`.
Los tiempos 0.30s, 0.27s y 0.31s pertenecen a ejecuciones distintas documentadas;
no se presentan como una sola corrida.

Las rutas relativas y hashes de logs, prompts, sesiones y otras fuentes
conservadas en los JSON son referencias de procedencia. **No implican que sus
originales estén publicados.** Los registros originales privados y los intentos
previos quedan fuera de este paquete; los TXT y JSON incluidos conservan los
valores necesarios para leer las evidencias mostradas. No se incluyen los
placeholders de captura ni el script histórico que depende de fuentes privadas.

Para repetir los casos con código, consultar el
[README de la versión manual](../../../s4/clase-sdd/README.md) y el
[README del snapshot P3](../../../s4/versiones/p3-base-55/README.md).
El snapshot conserva los defectos descubiertos después en P4 y los declara;
55 pruebas aprobadas no demuestran corrección para todas las entradas posibles.
Repetir las pruebas no reproduce los bytes de las capturas históricas ni la
conversación original con agy. Los hashes permiten comprobar integridad, no
probar ejecución, autoría personal, acceso docente o aceptación académica.

El código manual fue devuelto por una llamada real a agy y los procesos de
comparación fueron ejecutados por Codex. La ampliación de detalle en Spec Kit
incluyó una petición más precisa. Estas atribuciones y límites aparecen en los
registros; no se atribuyen percepciones ni experiencias personales al estudiante.
