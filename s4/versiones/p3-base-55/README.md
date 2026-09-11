# P3 — snapshot histórico de 55 pruebas

Esta copia reproduce la base de P3 antes de ampliar la auditoría en P4. Proviene
de `08-p3-reproducible`; `origen-sha256.json` registra hashes originales y de
las copias. Sólo se sanearon rutas absolutas de documentos. Fuentes Python,
pruebas, pyproject y uv.lock son copias exactas.

```bash
uv sync --frozen
uv run --frozen pytest tests/ -q
uv run --frozen python -m temperatura 0 C F
```

Resultado original: 55 aprobadas (19 unitarias, 27 integración en memoria,
9 e2e) y 108/122 líneas cubiertas. El bloque manual está en
[clase-sdd](../../clase-sdd/) y la comparación en [comparacion.md](../../comparacion.md).

## Limitaciones históricas identificadas después

P4 detectó y corrigió en la base canónica el desbordamiento de `abs(Decimal)`
con `1e9999999`, y el doble redondeo del valor
`1.0027777777777777777777777777 C F`. Este snapshot conserva esos comportamientos
para reproducir la etapa: no es la versión final recomendada. La versión
corregida vive en [mi-proyecto-speckit](../../mi-proyecto-speckit/).
