#!/usr/bin/env python3
"""Verificación de extremo a extremo de "Gastos" en vivo: REST + MCP (streamable-http con JWT).
Uso: e2e_gastos.py http://127.0.0.1:PUERTO"""
import asyncio
import json
import sys
import uuid

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

BASE = sys.argv[1].rstrip("/")
ok = True


def check(nombre, cond, detalle=""):
    global ok
    ok &= bool(cond)
    print(f"[{'OK' if cond else 'FALLA'}] {nombre} {detalle}")


def main():
    email = f"e2e-{uuid.uuid4().hex[:6]}@ejemplo.com"
    clave = "clave-e2e-" + uuid.uuid4().hex[:8]
    c = httpx.Client(base_url=BASE, timeout=20)
    r = c.post("/usuarios/", json={"email": email, "password": clave}); check("registro 201", r.status_code == 201, r.text)
    r = c.post("/usuarios/", json={"email": email, "password": clave}); check("email duplicado 400", r.status_code == 400, r.text)
    r = c.post("/usuarios/token", data={"username": email, "password": "mala"}); check("login inválido 401", r.status_code == 401)
    r = c.post("/usuarios/token", data={"username": email, "password": clave}); check("login 200", r.status_code == 200)
    tok = r.json()["access_token"]; H = {"Authorization": f"Bearer {tok}"}
    r = c.get("/gastos/"); check("GET sin token 401", r.status_code == 401)
    r = c.post("/gastos/", json={"descripcion": "Almuerzo", "monto": 12.5, "categoria": "comida"}); check("POST sin token 401", r.status_code == 401)
    r = c.post("/gastos/", json={"descripcion": "Almuerzo", "monto": 12.5, "categoria": "comida"}, headers=H); check("crear 201", r.status_code == 201, r.text)
    check("GastoOut sin usuario_id", "usuario_id" not in r.json())
    r = c.post("/gastos/", json={"descripcion": "X", "monto": -5, "categoria": "comida"}, headers=H); check("monto negativo 400", r.status_code == 400, r.text)
    r = c.post("/gastos/", json={"descripcion": "  ", "monto": 5, "categoria": "comida"}, headers=H); check("descripción vacía 400", r.status_code == 400, r.text)
    r = c.post("/gastos/", json={"descripcion": "X", "monto": 5, "categoria": "salud"}, headers=H); check("categoría inválida 400", r.status_code == 400, r.text)
    r = c.post("/gastos/", json={"descripcion": "Cena", "monto": 490, "categoria": "comida"}, headers=H); check("límite 500 excedido 400", r.status_code == 400, r.text)
    r = c.get("/gastos/?limit=0", headers=H); check("limit=0 422", r.status_code == 422)
    r = c.get("/gastos/?usuario_id=999", headers=H); check("usuario_id ajeno ignorado", r.status_code == 200 and len(r.json()) == 1, r.text)
    r = c.post(f"{BASE}/mcp/", headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}, content="{}"); check("MCP sin token 401", r.status_code == 401)

    async def mcp_flujo(token, espera_usuario=True):
        http_client = httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"})
        async with streamable_http_client(f"{BASE}/mcp/", http_client=http_client) as (rd, wr, _):
            async with ClientSession(rd, wr) as s:
                await s.initialize()
                tools = await s.list_tools()
                return s, tools, rd, wr

    async def mcp_prueba():
        http_client = httpx.AsyncClient(headers={"Authorization": f"Bearer {tok}"})
        async with streamable_http_client(f"{BASE}/mcp/", http_client=http_client) as (rd, wr, _):
            async with ClientSession(rd, wr) as s:
                await s.initialize()
                tools = await s.list_tools()
                nombres = sorted(t.name for t in tools.tools)
                check("MCP tools", nombres == ["listar_gastos", "registrar_gasto"], str(nombres))
                x = await s.call_tool("registrar_gasto", {"descripcion": "Taxi MCP", "monto": 7.25, "categoria": "transporte"})
                check("MCP registrar_gasto éxito", "Taxi MCP" in x.content[0].text and not x.isError, x.content[0].text.replace("\n", " "))
                x = await s.call_tool("registrar_gasto", {"descripcion": "X", "monto": 3, "categoria": "inventada"})
                check("MCP error de negocio estructurado", '"error"' in x.content[0].text, x.content[0].text.replace("\n", " "))
                x = await s.call_tool("listar_gastos", {"skip": 0, "limit": 10})
                check("MCP listar_gastos", "Taxi MCP" in json.dumps(x.structuredContent or x.content[0].text), "")
    asyncio.run(mcp_prueba())
    r = c.get("/gastos/", headers=H); check("gasto creado por MCP visible por REST", any(g["descripcion"] == "Taxi MCP" for g in r.json()), r.text)
    print("RESULTADO:", "TODO OK" if ok else "HAY FALLAS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
