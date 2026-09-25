#!/usr/bin/env python3
"""Verificación de extremo a extremo del Inventario en vivo: REST + MCP (streamable-http con JWT).
Uso: e2e_inventario.py http://127.0.0.1:PUERTO"""
import asyncio
import json
import sys
import uuid

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.types import ElicitResult

BASE = sys.argv[1].rstrip("/")
ok = True


def check(nombre, cond, detalle=""):
    global ok
    ok &= bool(cond)
    print(f"[{'OK' if cond else 'FALLA'}] {nombre} {detalle}"[:170])


def usuario(c):
    email, clave = f"e2e-{uuid.uuid4().hex[:6]}@ejemplo.com", "clave-" + uuid.uuid4().hex[:10]
    c.post("/usuarios/", json={"email": email, "password": clave})
    tok = c.post("/usuarios/token", data={"username": email, "password": clave}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}, tok


def main():
    c = httpx.Client(base_url=BASE, timeout=20)
    H, tok = usuario(c)
    H2, _ = usuario(c)
    r = c.get("/productos/"); check("GET sin token 401", r.status_code == 401)
    r = c.post("/productos/", json={"nombre": "Tóner Negro", "cantidad": 6, "cantidad_minima": 5}, headers=H)
    check("crear 201", r.status_code == 201, r.text); p = r.json(); pid = p["id"]
    check("crear: sin usuario_id ni nombre_normalizado", "usuario_id" not in p and "nombre_normalizado" not in p)
    check("crear: 6 > 5 sin alerta", p["requiere_reposicion"] is False)
    r = c.post("/productos/", json={"nombre": " tóner negro ", "cantidad": 1, "cantidad_minima": 0}, headers=H); check("nombre repetido (mayúsculas y espacios) 400", r.status_code == 400, r.text)
    r = c.post("/productos/", json={"nombre": "Tóner Negro", "cantidad": 1, "cantidad_minima": 0}, headers=H2); check("mismo nombre en otro usuario 201", r.status_code == 201)
    r = c.post("/productos/", json={"nombre": "   ", "cantidad": 1, "cantidad_minima": 0}, headers=H); check("nombre vacío 400", r.status_code == 400, r.text)
    r = c.post("/productos/", json={"nombre": "", "cantidad": 1, "cantidad_minima": 0}, headers=H); check('nombre "" 400 (services, no schema)', r.status_code == 400, r.text)
    r = c.post("/productos/", json={"nombre": "Papel", "cantidad": -1, "cantidad_minima": 0}, headers=H); check("cantidad negativa 400 (services, no schema)", r.status_code == 400, r.text)
    r = c.post(f"/productos/{pid}/ajustar", json={"cantidad": -1, "motivo": "entrega a oficina"}, headers=H)
    check("ajuste deja 5 = mínimo -> alerta (<=)", r.status_code == 200 and r.json()["cantidad"] == 5 and r.json()["requiere_reposicion"] is True, r.text)
    r = c.post(f"/productos/{pid}/ajustar", json={"cantidad": 0}, headers=H); check("ajuste cero 400", r.status_code == 400, r.text)
    r = c.post(f"/productos/{pid}/ajustar", json={"cantidad": -6}, headers=H); check("stock insuficiente 400", r.status_code == 400, r.text)
    r = c.get(f"/productos/{pid}", headers=H); check("rechazo atómico: sigue en 5", r.json()["cantidad"] == 5)
    r = c.post(f"/productos/{pid}/ajustar", json={"cantidad": -5}, headers=H); check("saldo exacto 0 permitido", r.status_code == 200 and r.json()["cantidad"] == 0, r.text)
    r = c.get("/productos/alertas", headers=H); check("alertas lista el producto", any(x["id"] == pid for x in r.json()), r.text)
    r = c.post(f"/productos/{pid}/ajustar", json={"cantidad": 10}, headers=H); check("entrada de stock sale de alerta", r.json()["requiere_reposicion"] is False, r.text)
    r = c.patch(f"/productos/{pid}", json={"cantidad": 99}, headers=H); check("PATCH con cantidad 422", r.status_code == 422)
    r = c.patch(f"/productos/{pid}", json={"cantidad_minima": 12}, headers=H); check("PATCH mínimo 200 y alerta recalculada", r.status_code == 200 and r.json()["requiere_reposicion"] is True, r.text)
    r = c.get(f"/productos/{pid}", headers=H2); check("producto ajeno 403", r.status_code == 403)
    r = c.post(f"/productos/{pid}/ajustar", json={"cantidad": 1}, headers=H2); check("ajustar ajeno 403", r.status_code == 403)
    r = c.delete(f"/productos/{pid}", headers=H2); check("eliminar ajeno 403", r.status_code == 403)
    r = c.get("/productos/999999", headers=H); check("inexistente 404", r.status_code == 404)
    r = c.get("/productos/?limit=0", headers=H); check("limit=0 422", r.status_code == 422)
    r = c.post(f"{BASE}/mcp/", headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}, content="{}"); check("MCP sin token 401", r.status_code == 401)

    # Integridad del JWT: el servidor no puede confiar en un token que no verificó.
    import base64
    import jwt as pyjwt
    reclamos = pyjwt.decode(tok, options={"verify_signature": False})
    victima = int(pyjwt.decode(H2["Authorization"][7:], options={"verify_signature": False})["sub"])
    falso = pyjwt.encode({**reclamos, "sub": str(victima)}, uuid.uuid4().hex * 2, algorithm="HS256")
    cab, _, firma = tok.split(".")
    carga = base64.urlsafe_b64encode(json.dumps({**reclamos, "sub": str(victima)}).encode()).decode().rstrip("=")
    alterado = f"{cab}.{carga}.{firma}"
    sin_firma = pyjwt.encode({**reclamos, "sub": str(victima)}, None, algorithm="none")
    for nombre, t in (("firmado con otra clave (sub = otro usuario)", falso),
                      ("payload alterado sin volver a firmar", alterado),
                      ("alg=none sin firma", sin_firma)):
        r = c.get("/productos/", headers={"Authorization": f"Bearer {t}"}); check(f"JWT {nombre} -> REST 401", r.status_code == 401)
        r = c.post(f"{BASE}/mcp/", headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json", "Accept": "application/json, text/event-stream"}, content="{}")
        check(f"JWT {nombre} -> MCP 401", r.status_code == 401)

    async def flujo():
        http = httpx.AsyncClient(headers={"Authorization": f"Bearer {tok}"})
        async with streamable_http_client(f"{BASE}/mcp/", http_client=http) as (rd, wr, _):
            decision = {"valor": "decline"}

            async def cb(context, params):
                if decision["valor"] == "accept":
                    return ElicitResult(action="accept", content={"confirmar": True})
                return ElicitResult(action="decline")

            async with ClientSession(rd, wr, elicitation_callback=cb) as s:
                await s.initialize()
                nombres = sorted(t.name for t in (await s.list_tools()).tools)
                check("MCP tools", len(nombres) == 5, str(nombres))
                x = await s.call_tool("crear_producto", {"nombre": "Cable UTP (MCP)", "cantidad": 3, "cantidad_minima": 2})
                texto = x.content[0].text
                check("MCP crear_producto", "Cable UTP" in texto and not x.isError, " ".join(texto.split()))
                nuevo = json.loads(texto)["id"]
                x = await s.call_tool("ajustar_stock", {"producto_id": nuevo, "cantidad": -10})
                check("MCP error de negocio estructurado", '"error"' in x.content[0].text, " ".join(x.content[0].text.split()))
                x = await s.call_tool("listar_alertas_reposicion", {})
                check("MCP listar_alertas_reposicion", not x.isError)
                x = await s.call_tool("listar_productos", {"limit": 500})
                check("MCP paginación fuera de rango -> error del contrato", not x.isError and json.loads(x.content[0].text) == {"error": "Parámetros de paginación inválidos"}, " ".join(x.content[0].text.split()))
                x = await s.call_tool("crear_producto", {"nombre": "", "cantidad": 1, "cantidad_minima": 0})
                check("MCP nombre vacío -> error del contrato", not x.isError and json.loads(x.content[0].text) == {"error": "El nombre del producto no puede estar vacío"}, " ".join(x.content[0].text.split()))
                x = await s.call_tool("ajustar_stock", {"producto_id": nuevo, "cantidad": 1, "motivo": "x" * 300})
                check("MCP motivo demasiado largo -> {error}", not x.isError and "error" in json.loads(x.content[0].text), " ".join(x.content[0].text.split()))
                decision["valor"] = "decline"
                x = await s.call_tool("eliminar_producto", {"producto_id": nuevo})
                sigue = c.get(f"/productos/{nuevo}", headers=H).status_code == 200
                check("MCP eliminar rechazado: el producto sigue", sigue, " ".join(x.content[0].text.split()))
                decision["valor"] = "accept"
                x = await s.call_tool("eliminar_producto", {"producto_id": nuevo})
                borrado = c.get(f"/productos/{nuevo}", headers=H).status_code == 404
                check("MCP eliminar confirmado: el producto ya no existe", borrado, " ".join(x.content[0].text.split()))
    asyncio.run(flujo())
    r = c.get("/productos/", headers=H); check("REST ve lo creado por el mismo usuario", r.status_code == 200)
    r = c.delete(f"/productos/{pid}", headers=H); check("DELETE propio 204", r.status_code == 204)
    print("RESULTADO:", "TODO OK" if ok else "HAY FALLAS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
