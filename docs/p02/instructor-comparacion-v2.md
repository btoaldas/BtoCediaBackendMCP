# Comparación posterior verificada con la grabación — versión 2

Fuente: [VIDEO SESIÓN 3: 31 DE AGOSTO, AVAC](https://cursos.cedia.org.ec/mod/page/view.php?id=48522), video Vimeo 1223032852. Se consultaron la transcripción autogenerada y fotogramas pausados mediante el navegador autenticado. No se extrajeron cookies ni se hicieron solicitudes externas al navegador. Las predicciones propias ya estaban registradas y las cuatro rondas ejecutadas antes de esta consulta.

## Comparación acotada

| Etapa | Evidencia del instructor | Comparación con nuestra ejecución |
|---|---|---|
| Contraseña, 1:11:32 | Reporte visual válido, fuerza Muy Fuerte (100/100), entropía 111.4 bits. Nueve comprobaciones: mínimo 8, máximo 128, cuatro clases de caracteres, sin espacios, variedad suficiente (16 únicos) y ausencia en contraseñas comunes conocidas. | Coinciden los límites 8/128 y las reglas de composición/espacios. Nuestra dataclass devuelve is_valid/errors/strength y no puntuación sobre 100 ni entropía. No se comprobó igualdad de las listas de exclusión. |
| Vacío, comando previo visible en 1:20:15 | La terminal conserva una invocación del programa con argumento vacío y una despedida. La transcripción de 1:12:38–1:12:48 lo describe verbalmente como incorrecto. | El comportamiento visible de la CLI es salir, mientras nuestro ensayo directo de validate_password("") devuelve False y cinco errores. Se conserva la discrepancia entre narración y pantalla; no se infiere el exit code docente ni el resultado de su función interna. |
| Email, 1:18:05 y fotograma 1:20:15 | Archivo email_validator.py separado, clase EmailValidationResult, reporte con usuario/dominio/TLD y comprobaciones de máximo 254 total, 64 local y proveedores temporales. Un ejemplo institucional aparece con formato válido. | Nuestra ampliación permanece en un main.py y comparte ValidationResult con strength=None. Coinciden límites 254/64; no agregamos detección de proveedores temporales ni corrección de dominios comunes. No se verificaron en pantalla los tres mismos emails del ensayo propio. |
| Usuarios, 1:28:11 y 1:30:06 | Archivo examples/users_sample.json con una lista de objetos name/email/password. La respuesta ofrece UserManager, validate_users, lista en memoria y una opción de carga de JSON o CSV. | Nuestra ronda 3 usa User con username/email/password y una lista en memoria; no incorpora gestor de archivos. Esto compara la estructura y opciones visibles, no demuestra ausencia de regresiones en el código del instructor. |
| Administradores, 1:29:58 y 1:30:06 | La transcripción menciona la contraseña opcional para administradores y se ve el pedido de cierre en la guía. | No se confirmó una ejecución ni una falla del instructor después de ese cambio. Nuestra inconsistencia de is_admin como texto sí fue reproducida por dos vías; no se le atribuye al instructor. |

La frase sobre mínimo 12 caracteres en 36:18–37:17 pertenece a un ejemplo explicativo de spec, no al resultado de la ronda 1. Se descartó expresamente como base de esa comparación.

## Alcance de la conclusión

Los resultados no son idénticos en formato y estructura. Eso no permite atribuir las diferencias solamente a la ambigüedad del pedido: no se controlaron el modelo, contexto previo o canal de ejecución, y nuestro mensaje incluyó una envoltura operativa sin herramientas. La observación sí permite identificar decisiones que el pedido no especificaba y que cada generación resolvió de forma distinta.

Los registros y capturas propios anteriores dicen que el resultado del instructor no estaba disponible: reflejan el estado anterior a esta consulta. Se preservan sin retocarlos; este anexo actualiza el contraste después de la ejecución. No se afirma asistencia sincrónica ni se convierten las predicciones del asistente en experiencias personales del estudiante.

## Matriz de cierre actualizada

- Cuatro pedidos generados con agy real y código exacto conservado: comprobado.
- Predicciones del asistente anteriores a las llamadas: 4/4 comprobadas.
- Casos de la guía, dos usuarios y lista completa: comprobados.
- Falla del cierre desde función y entrada JSON por lote: comprobada; se conserva intencionalmente.
- Tres capturas reales del visor de registros (rondas 1, 2 y cierre): proporcionadas y verificadas por el coordinador documental. Son capturas del visor, no de la terminal ni del aula.
- Tres reflexiones asistidas, con atribución explícita y comparación posterior: preparadas en el insumo v2.
- Resultado específico del cierre del instructor: no verificado, límite declarado.
- Repositorio: no exigido por esta práctica.
