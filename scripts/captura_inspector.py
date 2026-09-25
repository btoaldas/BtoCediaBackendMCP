#!/usr/bin/env python3
"""Capturas reales de MCP Inspector (v2) con Playwright.

Requiere un Inspector ya levantado con catálogo temporal y secretos en memoria:
  MCP_INSPECTOR_SECRET_STORE=memory DANGEROUSLY_OMIT_AUTH=true MCP_AUTO_OPEN_ENABLED=false \
    npx -y @modelcontextprotocol/inspector --catalog /tmp/<dir>/mcp.json

Uso:
  captura_inspector.py --server-id ID --url http://127.0.0.1:PUERTO/mcp/ [--token-env VAR]
                       --out captura.png (--conectar | --tool NOMBRE [--args JSON] [--antes RUTA.png])
                       [--elicitacion aceptar|rechazar] [--campo-confirmar Confirmar]
El token se lee de la variable de entorno indicada: nunca se escribe en disco ni en la línea de comandos.
"""
import argparse
import json
import os
import sys
from playwright.sync_api import sync_playwright

INSPECTOR = "http://127.0.0.1:6274/"


def etiqueta(clave: str) -> str:
    return " ".join(p.capitalize() for p in clave.split("_"))


def asegurar_servidor(pg, sid, url):
    if pg.get_by_text(sid, exact=True).count():
        return
    pg.get_by_role("button", name="Add Servers").click()
    pg.get_by_role("menuitem").first.click()
    pg.get_by_role("textbox", name="Server ID").fill(sid)
    pg.get_by_role("textbox", name="Transport").click()
    pg.get_by_role("option", name="streamable-http").click()
    pg.get_by_role("textbox", name="URL").fill(url)
    pg.get_by_role("button", name="Add", exact=True).click()
    pg.wait_for_timeout(700)


def poner_cabecera(pg, sid, token):
    tarjeta = pg.locator("div").filter(has_text=sid).filter(has=pg.get_by_role("button", name="Settings")).last
    tarjeta.get_by_role("button", name="Settings").click()
    pg.wait_for_timeout(400)
    pg.get_by_role("button", name="Custom Headers").click()
    if pg.get_by_placeholder("Key").count() == 0:
        pg.get_by_role("button", name="+ Add Header").click()
    pg.get_by_placeholder("Key").first.fill("Authorization")
    pg.get_by_placeholder("Value").first.fill(f"Bearer {token}")
    pg.get_by_role("button", name="Close").click()
    pg.wait_for_timeout(400)


def conectar(pg, sid):
    interruptor = pg.get_by_label(f'Connect or disconnect "{sid}"')
    if not interruptor.is_checked():
        interruptor.click(force=True)
    pg.get_by_text("Connected", exact=True).first.wait_for(timeout=20000)
    pg.wait_for_timeout(1200)


def llenar(pg, args):
    for clave, valor in args.items():
        nombre = etiqueta(clave)
        campo = pg.get_by_role("textbox", name=nombre)
        if campo.count() == 0:
            campo = pg.get_by_role("spinbutton", name=nombre)
        campo.first.fill(str(valor))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server-id", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--token-env")
    ap.add_argument("--out", required=True)
    ap.add_argument("--conectar", action="store_true")
    ap.add_argument("--tool")
    ap.add_argument("--args", default="{}")
    ap.add_argument("--antes")
    ap.add_argument("--elicitacion", choices=["aceptar", "rechazar"])
    ap.add_argument("--elicitacion-captura")
    a = ap.parse_args()
    token = os.environ.get(a.token_env, "") if a.token_env else ""
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": 1440, "height": 950}, device_scale_factor=2)
        pg.goto(INSPECTOR, wait_until="domcontentloaded")
        pg.wait_for_selector("text=Servers", timeout=20000)
        pg.wait_for_timeout(800)
        asegurar_servidor(pg, a.server_id, a.url)
        if token:
            poner_cabecera(pg, a.server_id, token)
        conectar(pg, a.server_id)
        if a.conectar:
            pg.screenshot(path=a.out)
            print(a.out)
            nav.close()
            return 0
        pg.get_by_text("Tools", exact=True).first.click()
        pg.wait_for_timeout(800)
        pg.get_by_text(a.tool, exact=True).first.click()
        pg.wait_for_timeout(700)
        llenar(pg, json.loads(a.args))
        if a.antes:
            pg.screenshot(path=a.antes)
        pg.get_by_role("button", name="Execute Tool").click()
        if a.elicitacion:
            dialogo = pg.get_by_role("dialog").last
            dialogo.wait_for(timeout=15000)
            pg.wait_for_timeout(600)
            if a.elicitacion_captura:
                pg.screenshot(path=a.elicitacion_captura)
            if a.elicitacion == "aceptar":
                casillas = dialogo.get_by_role("checkbox")
                if casillas.count():
                    casillas.first.check(force=True)
                dialogo.get_by_role("button", name="Accept").or_(dialogo.get_by_role("button", name="Submit")).first.click()
            else:
                dialogo.get_by_role("button", name="Decline").first.click()
        pg.get_by_text("Results", exact=True).first.wait_for(timeout=20000)
        pg.wait_for_timeout(900)
        pg.screenshot(path=a.out)
        print(a.out)
        nav.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
