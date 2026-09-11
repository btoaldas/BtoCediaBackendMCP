# Procedencia y avisos de terceros

Este documento identifica componentes de terceros conservados en el laboratorio académico. No establece una licencia general para el repositorio ni atribuye una licencia abierta al código académico propio o al contenido docente.

## GitHub Spec Kit

- Proyecto oficial: [github/spec-kit](https://github.com/github/spec-kit).
- Revisión utilizada: [`c173bf19a6654e3b05386ec3599349a55282b897`](https://github.com/github/spec-kit/tree/c173bf19a6654e3b05386ec3599349a55282b897), obtenida mediante `uv`.
- Titular indicado por el archivo oficial: **Copyright GitHub, Inc.**
- Licencia declarada: **MIT**.
- Texto íntegro conservado en [LICENSES/spec-kit-MIT.txt](LICENSES/spec-kit-MIT.txt).
- Fuente exacta: [LICENSE del commit](https://raw.githubusercontent.com/github/spec-kit/c173bf19a6654e3b05386ec3599349a55282b897/LICENSE).
- SHA-256 del archivo de licencia, sin modificar: `2510b446bc1f0cf9702453075d20cd88631e20e5642658edb7325d9c1eb534f7` (1060 bytes).

Se verificó la igualdad de bytes entre la fuente oficial, `LICENSE` del checkout local usado por `uv`, el objeto Git de esa revisión y la copia incluida en `LICENSES/`.

Los scripts y plantillas importados bajo `s4/mi-proyecto-speckit/.specify/`, y las skills `s4/mi-proyecto-speckit/.agents/skills/speckit-*/`, proceden de Spec Kit. Son material de terceros o derivados de sus plantillas; no se presentan como creación original del estudiante. El inventario de integración de scripts y plantillas está en `s4/mi-proyecto-speckit/.specify/integrations/speckit.manifest.json`.

Las skills instaladas son `speckit-analyze`, `speckit-checklist`, `speckit-clarify`, `speckit-constitution`, `speckit-converge`, `speckit-implement`, `speckit-plan`, `speckit-specify`, `speckit-tasks` y `speckit-taskstoissues`. La licencia y el aviso de copyright de Spec Kit deben acompañar las copias o porciones sustanciales de su software, conforme al texto íntegro adjunto.

La presencia de un archivo en `.specify/` no extiende automáticamente esta atribución a contenidos propios del ejercicio, como decisiones de la constitución o requisitos redactados durante la práctica. Deben distinguirse las plantillas de origen y el contenido académico añadido. El software de Spec Kit se suministra con las exclusiones de garantía y responsabilidad del texto MIT adjunto.

## Guía docente de CEDIA y copia del script de reporte

Procedencia: guía de la sesión 5 del curso **Programación de Backend y MCP en Python para IA Generativa**, titulada **Guía Práctica — Pruebas, Cobertura y Seguridad (con Skills, Agentes y Hooks)**, obtenida del AVAC de CEDIA y conservada localmente como `materiales/practica-04.md`.

El archivo `s4/mi-proyecto-speckit/.agents/skills/qa-report/generar_reporte_guia_original.py` conserva el script Python de esa guía. Se comprobó que coincide con su bloque de código, salvo la normalización de espacios exteriores al comparar. SHA-256 de la copia local: `387dae86387829603c30338c12de2aeec56a379df62e4ce493cd3af7b1e360d8`.

**No se ha identificado una licencia abierta para esa guía ni para el script docente.** No se les aplica la licencia MIT de Spec Kit y no se afirma que sean dominio público. La autoría docente se reconoce por su procedencia; no se inventa un titular personal ni una autorización de redistribución.

La copia original se preserva localmente para trazabilidad y entrega académica privada. Se recomienda **excluir `s4/mi-proyecto-speckit/.agents/skills/qa-report/generar_reporte_guia_original.py` de cualquier publicación remota**, sin borrar el archivo local. Su eventual inclusión pública requiere una base de autorización o licencia verificable. Este aviso no cambia el estado de seguimiento en Git ni publica archivos.

Las adaptaciones o fragmentos de contenido docente que permanezcan en otros archivos necesitan la misma revisión de procedencia antes de una distribución pública; cambiar el nombre o modificar el original no convierte por sí solo el material en una obra con licencia abierta.

## Alcance

No se concede aquí una licencia al código académico propio, a las evidencias, a las grabaciones ni a otros materiales del curso. La redistribución de cada componente debe respetar su procedencia y los permisos que efectivamente consten. Los avisos de dependencias instaladas mediante gestores de paquetes siguen rigiéndose por sus respectivas licencias.
