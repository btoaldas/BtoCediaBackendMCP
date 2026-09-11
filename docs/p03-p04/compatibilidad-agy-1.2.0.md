# Compatibilidad comprobada con Antigravity CLI 1.2.0

Se conservaron los siete skills y tres archivos agent.md de la guía. En esta
instalación, los primeros subagentes cargados no dispusieron de ejecución.
El principal los terminó y algunas pruebas las ejecutó él: esas corridas no se
atribuyen al tester. Luego se definieron roles transitorios reales con
DefineSubagent, usando `enable_write_tools=true` y los alias `tester-agent-native`,
`security-agent-native` y `report-agent-native`. Las definiciones transitorias no
son archivos adicionales persistentes ni un cambio de configuración global.
Los permisos de cada acción siguieron siendo revisados en el CLI.

La [documentación oficial de subagentes](https://www.antigravity.google/docs/subagents/)
consultada el 10 de septiembre de 2026 describe `tools` en frontmatter y advierte
sobre nombres no reconocidos. Esto difiere de la afirmación de la guía sobre la
ausencia de ese campo. La lista general no demuestra qué nombres acepta cada
versión del CLI; no se agregó una allowlist supuesta. La
[documentación de colaboración](https://www.antigravity.google/docs/hooks/)
distingue la capacidad dinámica `enable_write_tools` de la configuración Markdown.
La evidencia de esta práctica es la definición nativa seguida de permisos y
comandos reales, no una inferencia de la documentación.

Para reproducir la adaptación dentro de agy, tras abrir la carpeta del proyecto,
indicar al principal:

> Lee los tres agent.md locales. Define subagentes nativos transitorios con esos
> mismos roles y system_prompt, usando la herramienta real DefineSubagent con
> enable_write_tools=true y alias terminados en -native. Conserva los permisos por
> acción. Invoca tester, espera su resultado, luego security y finalmente report.
> No sustituyas un subagente sin ejecución por una respuesta del principal. Si
> hay una aprobación pendiente, espera a que el operador la resuelva.

En la TUI se verificaron `Ctrl+K` para aprobar la petición pendiente de un
subagente y `Alt+J` para inspeccionarlo. La opción de permitir `uv run pytest`
se limitó a la conversación del escenario E; no se guardó una regla global.

La ruta ejecutada fue Setup → A → B → E, permitida expresamente por la guía.
En E, el principal corrigió el fallo de formato a partir del Stop real, después
se diagnosticaron y corrigieron excepciones genéricas, se revisó seguridad otra
vez, el tester verificó la versión final y report-agent ejecutó el reportador.
Se conservó además una pasada por capas con JSON separados para probar la
atribución de los comandos al tester. No se afirman tiempos de clase ni una
orquestación sin intervención humana: hubo adaptación y permisos del runtime.
