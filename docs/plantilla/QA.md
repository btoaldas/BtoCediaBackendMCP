# Verificación del generador

Prueba realizada el 10 de septiembre de 2026 con el runtime documental bundled. Se conservó la plantilla original y se usó exclusivamente contenido marcado como prueba técnica.

## Resultado

- PDF de prueba: dos páginas; texto, fecha, reflexión y enlace comprobados con `pypdf`.
- DOCX editable: una imagen y una tabla; dos páginas al renderizar con LibreOffice bundled.
- Inspección visual de todas las páginas: sin recortes, solapamientos o tabla rota. Se corrigieron la línea heredada del estilo Title y la sustitución tipográfica de Helvetica a una fuente con serifas en Word.
- Nueve comprobaciones satisfactorias: rechazo de final con simulación, hash incorrecto, fecha futura, imagen inexistente y URL con credenciales; rechazo de salida existente conservando todos sus hashes; extracción de texto de ambos PDF; estructura DOCX.
- Hash SHA-256 de la plantilla inspeccionada: `ce4ee35613a8a669e149f68a022d7fd9fc2de06e4461620308df06e523102560`.

## Evidencia local de la prueba

Los archivos de QA están excluidos del repositorio en `.tmp/qa-reportes-20260910/`: entrada `datos-prueba.json`, versiones `salida-v1` y `salida-v2`, renders `docx-v2`, entradas negativas y `validacion-v2.json`. No son informes del estudiante ni entregables para AVAC.

Para reproducir la generación se debe seleccionar una carpeta de salida todavía inexistente:

```bash
python scripts/reportes_curso.py .tmp/qa-reportes-20260910/datos-prueba.json --validar
python scripts/reportes_curso.py .tmp/qa-reportes-20260910/datos-prueba.json --salida .tmp/qa-reportes-repeticion
```

Para inspección final usar `render_docx.py` del skill documental. Su resolver selecciona automáticamente el ejecutable bundled `dependencies/bin/override/soffice` cuando se ejecuta con el Python bundled. No usar el LibreOffice desktop del usuario. El PDF se renderiza con Poppler bundled. Una entrada nueva con evidencias de otra práctica requiere una nueva revisión visual de todas sus páginas.

## Validación proporcional por práctica

Actualización del 10 de septiembre de 2026, 20:01: se contrastaron los entregables de las cuatro guías y se corrigió el requisito de repositorio para P2. Se añadió `docs/plantilla/test_guardias_reportes.py`: **13 tests satisfactorios**, con dobles de prueba explícitos de lectura e imagen, sin producir informes finales ficticios. Incluyen repositorio opcional en P2, al menos dos rondas y cierre, tres reflexiones, repositorio obligatorio P1/P3/P4, evidencias específicas, tabla P3 y rechazo de simulación/evidencia no verificada en las cuatro prácticas.

```bash
python docs/plantilla/test_guardias_reportes.py
```

Se generó además un artefacto **de prueba** P2 en `.tmp/qa-reportes-20260910/p2-sin-repo-salida/`, con renders `p2-sin-repo-docx/` y `p2-sin-repo-pdf-*`. Ambos formatos tienen dos páginas; se inspeccionaron todas y se comprobó por extracción que no incluyen `Enlace del repositorio` ni `Pendiente de publicar`. El DOCX mantiene texto editable, imagen y tabla. Los datos de este QA no representan trabajo académico ni experiencias del estudiante.
