# Práctica 2 — resultado final del experimento sin spec

Informe enviado para calificar el 10/09/2026 a las 20:45; descarga AVAC idéntica al PDF final revisado. Los cuatro snapshots de `rondas/01-contrasenas` a `rondas/04-administradores` contienen exactamente el código que devolvió agy. La carpeta `experimento` conserva la configuración Python y las dependencias bloqueadas para ejecutar las comprobaciones. El esqueleto inicial está preservado en el histórico local y Git previo.

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

[Notas y predicciones originales](notas.md) · [Comparación vigente con el instructor](../docs/p02/instructor-comparacion-v2.md) · [QA del informe final](../docs/p02/QA-entrega-v1.md) · [Salidas conservadas](../evidencia/p02/). El PDF, Word y comprobante AVAC identificados se conservan en el respaldo privado. Los logs del proveedor y sus estados locales permanecen fuera del material público.
