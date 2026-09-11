"""Renderiza extractos de logs reales; NO fabrica capturas de una interfaz."""
import html
import json
from pathlib import Path
import textwrap
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
EV = BASE / "evidencia/p02"
FONT = "/System/Library/Fonts/Menlo.ttc"
panels = []
for number in range(1, 5):
    prediction = json.loads((EV / f"prediccion-{number:02}.json").read_text())
    original = (EV / f"resultado-{number:02}.txt").read_text()
    lines = original.splitlines()
    selected = []
    for line in lines:
        if number == 1:
            if line.startswith("EJECUCIÓN"):
                selected.append(line)
            elif line.startswith('{"input":') and json.loads(line)["input"] in ["12345", "password", ""]:
                selected.append(line)
        elif number == 2:
            if line.startswith("EJECUCIÓN") or line.startswith('{"email":') or line.startswith("3 emails"):
                selected.append(line)
        elif number == 3:
            if line.startswith(("EJECUCIÓN", "DOS USUARIOS", "[{", '{"usuario":', "REGRESIÓN", "REGLA NO PEDIDA")):
                selected.append(line)
        else:
            if line.startswith(("EJECUCIÓN", "FALLA OBSERVADA", "CAUSA", "La hipótesis")):
                selected.append(line)
            elif line.startswith('{"caso":') and json.loads(line)["caso"] in ["booleano_false", "cadena_false", "admin_email_invalido"]:
                selected.append(line)
    if number == 4:
        second = (EV / "falla-reproducida.txt").read_text().splitlines()
        selected += [line for line in second if line.startswith(("tipo is_admin:", "validez", "AssertionError:", "EXIT_CODE="))]
    parts = ["REGISTRO DE EJECUCIÓN REAL — extracto renderizado; no captura de UI",
             f"PRÁCTICA 2 / {'CIERRE' if number == 4 else f'RONDA {number}'}",
             "Autor de predicción: agente asistente Codex; no vivencia atribuida al estudiante.",
             "PREDICCIÓN PREVIA UTC: " + prediction["recorded_at_utc"],
             "PEDIDO LITERAL: " + prediction["prompt"]]
    parts += [key + ": " + str(value) for key, value in prediction["prediccion"].items()]
    parts += ["", "EXTRACTO DE SALIDA PYTHON REAL:"] + selected
    parts += ["", f"Fuentes originales: prediccion-{number:02}.json; resultado-{number:02}.txt"
              + ("; falla-reproducida.txt" if number == 4 else ""),
              "Comparación con el instructor: no disponible."]
    content = "\n".join(parts) + "\n"
    source = EV / f"registro-{number:02}.txt"
    with source.open("x") as handle:
        handle.write(content)
    wrapped = []
    for line in content.splitlines():
        wrapped += textwrap.wrap(line, width=108, replace_whitespace=False, drop_whitespace=False) or [""]
    width, margin, line_height = 1840, 65, 35
    img = Image.new("RGB", (width, margin * 2 + line_height * len(wrapped)), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, 26)
    draw.rectangle((0, 0, width, 17), fill="#164d62")
    for index, line in enumerate(wrapped):
        draw.text((margin, margin + index * line_height), line,
                  font=font, fill="#164d62" if index < 2 else "#152028")
    destination = EV / f"registro-{number:02}.png"
    if destination.exists():
        raise FileExistsError(destination)
    img.save(destination)
    panels.append(f'<article id="ronda-{number}"><h2>{html.escape(parts[1])}</h2>'
                  f'<p>Visor de evidencia conservada. La imagen es un registro renderizado de logs reales.</p>'
                  f'<img src="registro-{number:02}.png" alt="Registro de la ronda {number}">'
                  f'<details><summary>Fuente textual completa del registro</summary><pre>{html.escape(content)}</pre></details></article>')
    print(destination.relative_to(BASE), img.size)
page = ('<!doctype html><html lang="es"><meta charset="utf-8"><title>Práctica 2 — evidencia real</title>'
        '<style>body{font:18px system-ui;margin:2rem;background:#eef3f5;color:#153342}h1{font-size:30px}'
        'article{background:white;padding:25px;margin:30px auto;max-width:1400px;border:1px solid #bbcbd1}'
        'img{width:100%;height:auto}pre{white-space:pre-wrap;font:15px monospace}a{color:#165a78}</style>'
        '<h1>Práctica 2: evolución registrada</h1><p>Predicciones del asistente antes de cada llamada real a agy. '
        'No se afirma participación sincrónica ni comparación disponible con el instructor.</p>'
        '<nav>' + ' · '.join(f'<a href="#ronda-{i}">{"Cierre" if i == 4 else "Ronda " + str(i)}</a>' for i in range(1, 5))
        + '</nav>' + ''.join(panels) + '</html>')
with (EV / "visor-evidencia.html").open("x") as handle:
    handle.write(page)
