# Inventario de prácticas 5 a 7

Consulta del 10 de septiembre de 2026, 19:51, America/Guayaquil. Fuente: semana 3 del curso **MOD2 Programación de Backend y MCP en Python para IA Generativa (08-26)**, curso 932, en la sesión autenticada del AVAC CEDIA.

Estado: **materiales identificados, contenido pendiente por bloqueo del navegador**. No se obtuvieron los originales y no se crearon archivos sustitutos en `materiales/`.

## Recursos oficiales identificados

Página de la semana: <https://cursos.cedia.org.ec/course/view.php?id=932&section=5>.

| Práctica | Título visible | Recurso oficial | Archivo de destino observado |
|---|---|---|---|
| 05 | Cimientos de un backend serio | <https://cursos.cedia.org.ec/mod/resource/view.php?id=48935> | `practica_05.md` |
| 06 | De la arquitectura al código | <https://cursos.cedia.org.ec/mod/resource/view.php?id=49000> | `practica_06.md` |
| 07 | Del backend a los agentes | <https://cursos.cedia.org.ec/mod/resource/view.php?id=49015> | `practica_07.md` |

Direcciones finales devueltas por la navegación del curso:

- Práctica 05: <https://cursos.cedia.org.ec/pluginfile.php/101755/mod_resource/content/3/practica_05.md>
- Práctica 06: <https://cursos.cedia.org.ec/pluginfile.php/101938/mod_resource/content/4/practica_06.md>
- Práctica 07: <https://cursos.cedia.org.ec/pluginfile.php/101968/mod_resource/content/1/practica_07.md>

Las versiones `3`, `4` y `1` proceden de las redirecciones observadas; no se probaron variantes adivinadas de URL.

## Requisitos y entregables

El contenido de los tres archivos no llegó a mostrarse. Por tanto, todavía **no se conocen** los enunciados exactos, productos de entrega, estructura de carpetas, pruebas exigidas, restricciones técnicas, rúbrica ni dependencias entre prácticas. El título no basta para deducirlos.

En la sección visible se encontraron los tres recursos de práctica y un cuestionario denominado **Prueba**. No apareció una actividad de entrega separada para P5, P6 o P7 en esa sección. Esto describe únicamente la página inspeccionada; no demuestra que no exista una instrucción de entrega en los Markdown.

Como material teórico asociado por título, la misma página ofrece:

- **Cimientos de un backend serio**, recurso 48934.
- **De la arquitectura al código**, recurso 48998.
- **Del backend a los agentes**, recurso 49014.

La correspondencia de títulos está confirmada en la página. No se inspeccionó el contenido teórico y no se atribuye una dependencia obligatoria sin el enunciado.

## Diagnóstico reproducible

1. Se abrió una pestaña propia en Edge para la semana 3, sin operar la pestaña principal de trabajo.
2. El clic normal de P5 y las navegaciones oficiales de P6 y P7 redirigieron a los Markdown anteriores.
3. Las tres mostraron una página del navegador con **Microsoft Edge bloqueó esta página** y `ERR_BLOCKED_BY_CLIENT`; el árbol accesible identificó `chrome-error://chromewebdata/`.
4. Para P5 también se solicitó una descarga mediante la API soportada `downloadMedia` sobre el enlace original del curso. La página permaneció en el curso y no se encontró un archivo nuevo correspondiente en Downloads. No se declaró éxito a partir de la llamada sin resultado.
5. La consulta del gestor `edge://downloads/all` fue rechazada por la política de URL de Browser Use. No se intentó acceder al gestor por otro medio ni se modificó ninguna protección.

El error confirma el bloqueo en el cliente, pero **no identifica qué extensión, política o componente lo causa**. Tampoco demuestra que el archivo del servidor esté ausente o dañado. No se extrajeron cookies, no se usaron peticiones HTTP fuera del navegador y no se desactivó seguridad.

## Próxima acción necesaria

Obtener los tres archivos originales mediante una descarga realizada por el usuario con sus controles normales, o mediante una copia suministrada por el docente. Guardarlos en las rutas reservadas `materiales/practica_05.md`, `materiales/practica_06.md` y `materiales/practica_07.md`, preservando cualquier archivo previo si apareciera.

Después de disponer de los originales: comprobar nombre, bytes y SHA-256; leer los enunciados completos; incorporar requisitos y entregables literales; determinar las dependencias reales; y solo entonces implementar las prácticas. No marcar las actividades como completadas mientras ese trabajo esté pendiente.
