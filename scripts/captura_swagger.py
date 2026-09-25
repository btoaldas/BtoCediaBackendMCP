#!/usr/bin/env python3
"""Capturas reales de Swagger UI (/docs) con Playwright + Chromium.

Uso: captura_swagger.py --base URL --out DIR --prefijo NOMBRE [--usuario EMAIL --clave CLAVE]
                         --op "METODO RUTA" [--body JSON] [--param nombre=valor ...] [--sin-auth]

Abre /docs, opcionalmente autoriza con OAuth2 password (botón Authorize), ejecuta una
operación con "Try it out" y guarda la captura de la operación con su respuesta real.
La clave se recibe por argumento o por la variable CLAVE_SWAGGER; nunca se escribe en disco.
"""
import argparse
import os
import re
import sys
from playwright.sync_api import sync_playwright


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefijo", required=True)
    ap.add_argument("--usuario")
    ap.add_argument("--clave", default=os.environ.get("CLAVE_SWAGGER"))
    ap.add_argument("--op", required=True, help='Ej: "POST /gastos/"')
    ap.add_argument("--body")
    ap.add_argument("--param", action="append", default=[])
    ap.add_argument("--ancho", type=int, default=1280)
    a = ap.parse_args()
    metodo, ruta = a.op.split(" ", 1)
    os.makedirs(a.out, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": a.ancho, "height": 900}, device_scale_factor=2)
        pag.goto(f"{a.base}/docs", wait_until="networkidle")
        pag.wait_for_selector(".opblock", timeout=20000)
        if a.usuario:
            pag.click("button.authorize")
            pag.fill("#oauth_username", a.usuario)
            pag.fill("#oauth_password", a.clave or "")
            pag.click(".auth-btn-wrapper button.authorize")
            pag.wait_for_selector("text=Logout", timeout=15000)
            pag.click(".auth-btn-wrapper button.btn-done")
        bloque = pag.locator(f".opblock-{metodo.lower()}").filter(
            has=pag.locator(".opblock-summary-path", has_text=re.compile(rf"^{re.escape(ruta)}$")))
        bloque.first.locator(".opblock-summary").click()
        bloque.first.locator("button.try-out__btn").click()
        if a.body is not None:
            area = bloque.first.locator("textarea.body-param__text")
            area.fill(a.body)
        for par in a.param:
            nombre, valor = par.split("=", 1)
            bloque.first.locator(f'tr[data-param-name="{nombre}"] input').fill(valor)
        bloque.first.locator("button.execute").click()
        bloque.first.locator(".responses-inner .live-responses-table").wait_for(timeout=20000)
        pag.wait_for_timeout(600)
        # El bloque "Curl" repite el Bearer token completo: se oculta antes de capturar.
        bloque.first.evaluate("""b => {
            b.querySelectorAll('.curl-command').forEach(e => e.style.display = 'none');
            b.querySelectorAll('h4').forEach(h => { if (h.textContent.trim() === 'Curl') h.style.display = 'none'; });
        }""")
        pag.wait_for_timeout(200)
        scroll = pag.evaluate("window.scrollY")
        caja = bloque.first.bounding_box()
        fin = bloque.first.locator(".live-responses-table").bounding_box()
        destino = os.path.join(a.out, f"{a.prefijo}.png")
        pag.screenshot(path=destino, full_page=True, clip={
            "x": caja["x"], "y": caja["y"] + scroll, "width": caja["width"],
            "height": fin["y"] + fin["height"] - caja["y"] + 12})
        codigo = bloque.first.locator(".live-responses-table tbody .response-col_status").first.inner_text()
        print(f"{destino} -> respuesta {codigo.strip()}")
        nav.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
