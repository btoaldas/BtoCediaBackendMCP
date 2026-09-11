# Ajuste de ejecución, sin añadir reglas de negocio

El primer intento headless devolvió salida vacía porque `read_file` requería un permiso que no podía pedir. El modo interactivo presentó términos/uso de datos y quedó detenido sin aceptar.

Se usa el ejecutable real `agy --print` autenticado. La primera línea de cada mensaje es el pedido literal docente. Se añade una nota operativa: no usar herramientas y devolver el código para guardarlo y ejecutarlo externamente. En rondas siguientes se incluye el código de la ronda anterior como contexto; no se introducen políticas de contraseñas, formato de email o roles adicionales.

Es una adaptación del canal de ejecución, no una reproducción idéntica de la dinámica de aula: las llamadas son reales a agy, pero el guardado del código y pruebas los ejecuta Codex. La envoltura completa y cada respuesta se conservan. No afirmar equivalencia aceptada por el docente.
