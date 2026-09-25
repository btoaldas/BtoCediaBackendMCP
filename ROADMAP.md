# Roadmap

Actualizado 2026-09-10. Nivel L laboratorio.

## Entregas verificadas

Prácticas 1 a 4 enviadas para calificar y cuatro descargas AVAC idénticas a sus PDF finales. P1 conserva el 429 real no observado; P2 conserva su fallo experimental; P3 conserva la base de 55 pruebas; P4 cerró con 65 pruebas y 94,3 % de cobertura. Código y capturas están publicados y el commit P4 se instaló y probó desde un archivo Git nuevo.

El respaldo conjunto local de código, ocho PDF/Word, manifiestos y comprobantes está verificado en Obsidian. Se conservan los originales históricos por separado. Las calificaciones docentes aún están pendientes.

## Siguiente

Obtener `practica_05.md`, `practica_06.md` y `practica_07.md` para continuar con sus requisitos reales. La descarga automática de esos Markdown quedó bloqueada. Los tres PDF teóricos asociados ya fueron descargados, respaldados y revisados: 117 páginas; no contienen las guías completas. No se implementan actividades suponiendo enunciados desconocidos.

## Pendientes de decisión o evidencia

- P1: dos ensayos reales de 20 solicitudes no produjeron 429. Mantener la observación y consultar al docente sobre la evidencia o una comprobación adicional acotada; el tier y su cuota no se verificaron.
- P5–P7: obtener y leer los tres Markdown originales antes de implementar.
- Asistencia: requiere revisión del docente; no se modifica ni se afirma presencia sin evidencia.
- Calificaciones, semanas futuras y cierre: dependen del curso. Entrega registrada no equivale a aceptación académica.
- Obsidian: copia local e integridad verificadas; sincronización remota de OneDrive no comprobada.

Repositorio remoto autorizado y público: [btoaldas/BtoCediaBackendMCP](https://github.com/btoaldas/BtoCediaBackendMCP), rama `main`, con acceso anónimo comprobado.

## Aplicación del ciclo de software

1 Requerimientos L: guías y criterios observables. 2 Arquitectura L: CLI y módulos pequeños. 3 Datos L: datos sintéticos locales si práctica exige persistencia. 4 Seguridad L: entradas y secretos protegidos. 5 Infra no: solo laptop. 6 Entornos y pruebas L: Git local, uv, pytest, evidencia. 7 Observabilidad no servicio: logs de ejecución suficientes. 8 Pagos no: no hay cobros. 9 Correo no: sin envío. 10 Móvil no: solo Python. 11 Mantenimiento no producción: documentación de reproducción y dependencias bloqueadas.

## Semana 4 — Práctica 08 y Proyecto Integrador (actualizado 2026-09-24)

Pendientes en AVAC, ambos cierran el domingo 27/09/2026 23:59: Práctica 08 — Backend Spec-kit (49102, parte de Prácticas 0–30) y Proyecto Integrador (49098, 0–40). Las guías `practica_05.md` a `practica_09.md`, el PDF del Proyecto Integrador y la teoría de Semana 4 se descargaron el 24/09 con la sesión del aula (`materiales/guias/`, `materiales/semana-04/`). Grabaciones 1–10 en transcripción local (`materiales/grabaciones/`).

Estructura: `s6-s8/proyecto-curso` (Gastos guiado P5–P7, referencia y fuente de los tests S6–S8), `s9/proyecto-curso-speckit` (P8) y `s9/proyecto-integrador` (idea propia). Cada uno es un repositorio Git local independiente, excluido del repositorio del curso mediante `.git/info/exclude`; su publicación requiere decisión explícita.

Ciclo de software, nivel L (laboratorio, datos sintéticos, solo laptop):
1 Requerimientos L: guía P8, PDF del integrador y rúbrica; `spec.md` de Spec Kit como fuente.
2 Arquitectura L: monolito modular en capas (routers, mcp, services, repositories, models, schemas, utils), DIP por parámetro, MCP montado en FastAPI por streamable-http.
3 Datos L: SQLAlchemy + Alembic sobre SQLite; `database.py` portable a Postgres.
4 Seguridad L+: OAuth2 password + JWT HS256, bcrypt, `.env` + pydantic-settings, `.env.example`, identidad solo desde el JWT, 500 sin stack trace, Bearer en MCP.
5 Infra: no aplica, sin despliegue. La guía P9 (Docker/CI-CD) es recurso de la sesión 10, no entregable.
6 Entornos y pruebas L: Git por proyecto, `uv.lock`, pytest + pytest-cov con umbrales de la constitución, hook pre-commit del anexo P8.
7 Observabilidad L: logging de peticiones y errores de la guía S7.
8 Pagos, 9 Correo, 10 Móvil: no aplican.
11 Mantenimiento: sin producción; versiones fijadas documentadas (`bcrypt<4.1`, `mcp<2`).

Puertas: el flujo Spec Kit de cada proyecto es el objeto de la práctica y se ejecuta por delegación del usuario; la puerta final (publicar repositorios y enviar en AVAC) exige su visto bueno explícito.

### Estado 2026-09-25 (madrugada)

- Integrador: 40/40 tareas (fase 8 de revisión incluida), 167 pruebas, 99,53 % global, e2e 41/41, stdio con y
  sin token, clon limpio en verde. Informe borrador v02 con 24 capturas.
- P8: arreglo de pruebas que dependían del `.env` local; clon limpio en verde. Informe borrador v06.
- Siguiente puerta (del responsable): aprobar contenido, publicar repositorios y subir a AVAC.

### Estado 2026-09-25 (mañana)

- Publicados: [BtoCediaGastosSpeckit](https://github.com/btoaldas/BtoCediaGastosSpeckit) (P8) y
  [BtoCediaInventarioMCP](https://github.com/btoaldas/BtoCediaInventarioMCP) (integrador), verificados con clon anónimo.
- Informes finales generados; subida a AVAC pendiente de un nuevo inicio de sesión en el aula.

### Estado 2026-09-25 06:48 — entregado

- Práctica 08 y Proyecto Integrador «Enviado para calificar» en AVAC; archivos verificados por SHA-256 contra los
  locales. Queda la calificación del docente.
