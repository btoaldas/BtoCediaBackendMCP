# Práctica 2 — laboratorio de evolución sin spec

Los cuatro snapshots de `rondas/01-contrasenas` a `rondas/04-administradores` contienen exactamente el código que devolvió agy. `rondas/00-inicio` conserva el esqueleto inicial de uv. La carpeta `experimento` aporta el entorno Python; sus archivos iniciales no sustituyen a los snapshots.

Desde la raíz del proyecto:

```bash
uv run --project s3/experimento python s3/probar_ronda_01.py
uv run --project s3/experimento python s3/probar_ronda_02.py
uv run --project s3/experimento python s3/probar_ronda_03.py
uv run --project s3/experimento python s3/probar_ronda_04.py
uv run --project s3/experimento python s3/verificar_trazabilidad.py
```

Las comprobaciones anteriores describen el comportamiento observado. El contraejemplo intencional debe terminar con `AssertionError` y exit 1:

```bash
uv run --project s3/experimento python s3/demostrar_falla.py
```

La contraseña `12345` se rechaza directamente, pero pasa en un usuario construido desde JSON con `is_admin="false"`. El código generado confunde una cadena no vacía con un booleano verdadero. Se conserva la falla para analizarla; no hay autenticación ni servicio desplegado.

`llamar_ronda.py` registra una llamada nueva a agy y usa creación exclusiva para no sobrescribir evidencias. No es necesario volver a invocar IA para reproducir las pruebas. `preparar_registros.py` crea imágenes nuevas desde fuentes textuales existentes y se niega a sobrescribirlas; requiere Pillow del runtime documental. Son registros renderizados, no capturas simuladas.

Las notas están en `s3/notas.md`, el informe técnico en `docs/p02/informe.md`, las salidas en `evidencia/p02` y el insumo oficial en el directorio privado. Los logs del proveedor y sus estados locales se conservan fuera del material de entrega.
