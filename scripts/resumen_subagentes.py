#!/usr/bin/env python3
"""Subagentes reales registrados en los stream-json de agy: definición (define_subagent) y ejecución
(manage_subagents list: rol, tipo, conversación propia y estado). Uso: resumen_subagentes.py <carpeta>"""
import glob
import json
import os
import sys
import textwrap

carpeta = sys.argv[1]
vistos = {}
for archivo in sorted(glob.glob(os.path.join(carpeta, "*.jsonl"))):
    turno = os.path.basename(archivo).split(".")[0]
    for linea in open(archivo, encoding="utf-8"):
        try:
            ev = json.loads(linea)
        except json.JSONDecodeError:
            continue
        su = ev.get("step_update") or {}
        if su.get("step_type") != "tool" or su.get("state") != "DONE":
            continue
        info = su.get("tool_info") or {}
        if su.get("tool_name") == "define_subagent":
            p = info.get("parameters") or {}
            print(f"[{turno}] define_subagent -> {p.get('name')}")
            print(textwrap.fill(p.get("description", ""), 108, initial_indent="    límite: ", subsequent_indent="            "))
        elif su.get("tool_name") == "manage_subagents":
            salida = info.get("output", "")
            i = salida.find("[")
            try:
                lista = json.loads(salida[i:]) if i >= 0 else []
            except json.JSONDecodeError:
                lista = []
            for s in lista:
                cid = s.get("conversationId", "")
                estado = s.get("state")
                if vistos.get(cid) == estado:
                    continue
                vistos[cid] = estado
                print(f"[{turno}] subagente {s.get('type'):<13} rol: {s.get('role'):<34} conv: {cid[:8]}…  estado: {estado}")
