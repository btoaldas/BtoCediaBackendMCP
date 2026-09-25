#!/usr/bin/env python3
"""Ejecuta un turno de Antigravity CLI (agy) en modo print y conserva la evidencia.

Uso:
  agy_turno.py --dir PROYECTO --project ID --out CARPETA --etiqueta NOMBRE
               [--conv ID_CONVERSACION] [--model MODELO] (--prompt TEXTO | --prompt-file RUTA)

Guarda CARPETA/NN-etiqueta.jsonl (stream-json crudo) y CARPETA/NN-etiqueta.md
(prompt + respuesta final + métricas). Imprime la respuesta y el id de conversación.
"""
import argparse
import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys

AGY = shutil.which("agy") or str(pathlib.Path.home() / ".local/bin/agy")


def siguiente_numero(out: pathlib.Path) -> int:
    nums = [int(p.name[:2]) for p in out.glob("[0-9][0-9]-*.jsonl")]
    return (max(nums) + 1) if nums else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--etiqueta", required=True)
    ap.add_argument("--conv")
    ap.add_argument("--model")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    a = ap.parse_args()

    prompt = a.prompt if a.prompt is not None else pathlib.Path(a.prompt_file).read_text(encoding="utf-8")
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    n = siguiente_numero(out)
    base = out / f"{n:02d}-{a.etiqueta}"

    cmd = [AGY, "-p", prompt, "--project", a.project, "--dangerously-skip-permissions",
           "--output-format", "stream-json", "--print-timeout", "0"]
    if a.conv:
        cmd += ["--conversation", a.conv]
    if a.model:
        cmd += ["--model", a.model]

    inicio = dt.datetime.now().astimezone()
    with open(f"{base}.jsonl", "w", encoding="utf-8") as fh:
        proc = subprocess.run(cmd, cwd=a.dir, stdout=fh, stderr=subprocess.STDOUT, text=True)
    fin = dt.datetime.now().astimezone()

    resultado, conv, pasos = None, a.conv, []
    for linea in open(f"{base}.jsonl", encoding="utf-8"):
        try:
            ev = json.loads(linea)
        except json.JSONDecodeError:
            continue
        if ev.get("event") == "result":
            resultado = ev["result"]
            conv = resultado.get("conversation_id", conv)
        su = ev.get("step_update")
        if su and su.get("state") == "DONE" and su.get("step_type") not in ("agent_response",):
            pasos.append(su.get("step_type"))

    respuesta = (resultado or {}).get("response", "(sin resultado: revisar jsonl)")
    meta = {
        "etiqueta": a.etiqueta, "numero": n, "inicio": inicio.isoformat(), "fin": fin.isoformat(),
        "exit_code": proc.returncode, "conversation_id": conv, "project": a.project,
        "status": (resultado or {}).get("status"), "duracion_s": (resultado or {}).get("duration_seconds"),
        "usage": (resultado or {}).get("usage"), "modelo_solicitado": a.model or "predeterminado",
    }
    with open(f"{base}.md", "w", encoding="utf-8") as fh:
        fh.write(f"# Turno {n:02d} — {a.etiqueta}\n\n```json\n{json.dumps(meta, ensure_ascii=False, indent=1)}\n```\n\n")
        fh.write("## Prompt enviado a agy\n\n````text\n" + prompt + "\n````\n\n## Respuesta final de agy\n\n" + respuesta + "\n")
    print(respuesta)
    print(f"\n[agy_turno] {base.name} exit={proc.returncode} status={meta['status']} conv={conv} dur={meta['duracion_s']}", file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
