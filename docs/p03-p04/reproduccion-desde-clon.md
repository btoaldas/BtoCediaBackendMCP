# Reproducción desde un clon

El checkout público conserva el código, los tests, los agentes, las skills, el hook y los documentos de especificación. El puntero `.specify/feature.json` es estado local por checkout, ignorado por Spec Kit; no se fuerza su publicación.

Desde la raíz del repositorio:

```sh
cd s4/mi-proyecto-speckit
uv sync --frozen
agy
```

Dentro de agy, invocar `/qa-orchestrate` y atender los permisos por acción. Los roles leen `specs/*/spec.md`; `AGENTS.md` identifica `specs/001-conversor-temperatura/spec.md`. El flujo QA no depende del puntero local.

Para reanudar comandos `/speckit-*` en esta carpeta, seleccionar la especificación mediante la variable oficial:

```sh
export SPECIFY_FEATURE_DIRECTORY=specs/001-conversor-temperatura
bash .specify/scripts/bash/check-prerequisites.sh --paths-only --json
```

La resolución se comprobó sin variables heredadas adicionales: la raíz detectada fue la carpeta de este subproyecto, `FEATURE_DIR` apuntó a su especificación y `FEATURE_SPEC` existía. El modo `--paths-only` no persistió cambios. Esta comprobación de rutas complementa las ejecuciones QA documentadas; no se presenta como una nueva ejecución de agentes.
