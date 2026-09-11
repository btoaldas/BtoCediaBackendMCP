# Práctica 2: protocolo de laboratorio (nivel L)

Objetivo: ejecutar los cuatro pedidos literales de la guía, registrar antes una predicción del asistente, probar después y conservar la evolución. No se especifica de antemano una política de contraseñas, representación de usuarios ni contrato de resultados: esa ambigüedad es el objeto del ejercicio.

Ámbito: recuperación asincrónica asistida; las predicciones y reflexiones técnicas son del agente asistente. Las predicciones se registraron antes de disponer de la comparación del instructor. La consulta posterior está documentada en [instructor-comparacion-v2.md](instructor-comparacion-v2.md), con alcance limitado; no se afirma asistencia ni equivalencia con participación sincrónica.

Entorno elegido: Python 3.12 y uv, por requisito docente y familiaridad; biblioteca estándar suficiente para pruebas locales y datos sintéticos. No se ofrece servicio web, autenticación real, persistencia productiva ni facturación. No se usan datos personales ni credenciales nuevas. El código y la evidencia revisada están publicados en el repositorio GitHub autorizado; los informes identificados y originales privados se conservan fuera de Git.

Arquitectura del experimento: prompt literal → agy → código de laboratorio → Python → salida observada. Datos sintéticos en memoria; evidencias y snapshots en disco. El código generado se conserva sin imponer capas ni contrato antes de cada pedido, pues hacerlo invalidaría el experimento sin spec. Los hallazgos posteriores identificarán las fronteras reales. No existe API HTTP.

Prueba de cierre: casos de contraseña y email de la guía, dos usuarios, petición administradores, reproducción de cualquier inconsistencia observable, y comparación fiel con las predicciones prospectivas. Se conserva salida CLI y una segunda ejecución independiente. Se incorporaron tres capturas reales del visor de esos registros; su procedencia distingue el visor de una terminal original. El informe final fue enviado para calificar y su descarga se verificó.

Reversibilidad: snapshots aditivos de las cuatro rondas; no borrar ni retocar versiones ya capturadas. Logs de agy pueden contener estado local del proveedor y se revisarán antes de preparar un entregable. No credenciales en logs o informes.
