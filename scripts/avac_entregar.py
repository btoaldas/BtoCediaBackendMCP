#!/usr/bin/env python3
"""Entrega de una tarea de Moodle (mod_assign) por HTTP, con la sesión del navegador.

Uso:
  avac_entregar.py --cmid N --estado                         # solo lee el estado de la entrega
  avac_entregar.py --cmid N --simular --archivo A [...]      # lee el formulario y dice qué haría, sin enviar
  avac_entregar.py --cmid N --archivo A [--archivo B ...]    # sube los archivos y guarda la entrega (borrador)
  avac_entregar.py --cmid N --enviar                         # "Enviar para calificar" de lo ya guardado

La sesión llega por la variable de entorno MOODLE_COOKIE (por ejemplo «MoodleSession=…», copiada del navegador
con la sesión abierta). Nunca se imprime ni se escribe en disco.
"""
import argparse
import html
import json
import mimetypes
import os
import re
import sys
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

BASE = "https://cursos.cedia.org.ec"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"


class _Redireccion(urllib.request.HTTPRedirectHandler):
    """Sigue redirecciones sin enviar la cookie del aula a otros dominios."""

    def __init__(self, host: str, galleta: str):
        self.host, self.galleta = host, galleta

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        nueva = super().redirect_request(req, fp, code, msg, headers, newurl)
        if nueva is not None:
            nueva.remove_header("Cookie")
            if urllib.parse.urlparse(nueva.full_url).netloc == self.host:
                nueva.add_unredirected_header("Cookie", self.galleta)
        return nueva


class Sesion:
    def __init__(self, base: str, galleta: str):
        self.base = base.rstrip("/")
        self.host = urllib.parse.urlparse(self.base).netloc
        self.galleta = galleta
        self._abridor = urllib.request.build_opener(_Redireccion(self.host, galleta))

    def _abrir(self, url: str, datos: bytes | None = None) -> str:
        pet = urllib.request.Request(url, data=datos)
        pet.add_unredirected_header("Cookie", self.galleta)
        pet.add_header("User-Agent", UA)
        if datos is not None:
            pet.add_header("Content-Type", "application/x-www-form-urlencoded")
        with self._abridor.open(pet, timeout=30) as r:
            return r.read().decode("utf-8", "replace")

    def get(self, ruta: str, **params) -> str:
        url = f"{self.base}/{ruta.lstrip('/')}"
        return self._abrir(url + ("?" + urllib.parse.urlencode(params) if params else ""))

    def post(self, ruta: str, campos: list[tuple[str, str]]) -> str:
        return self._abrir(f"{self.base}/{ruta.lstrip('/')}", urllib.parse.urlencode(campos).encode())


def texto(fragmento: str) -> str:
    fragmento = re.sub(r"<script.*?</script>|<style.*?</style>", " ", fragmento, flags=re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", fragmento)).split())


def exigir_sesion(pagina: str) -> None:
    titulo = re.search(r"<title>(.*?)</title>", pagina, re.S)
    if titulo and "Entrar al sitio" in titulo.group(1):
        raise SystemExit("Sin sesión en el aula: inicia sesión en el navegador y repite.")


def sesskey(pagina: str) -> str:
    m = re.search(r'"sesskey":"([^"]+)"', pagina)
    if not m:
        raise SystemExit("No se encontró sesskey en la página.")
    return m.group(1)


def formulario(pagina: str, marcador: str) -> tuple[str, list[tuple[str, str]]]:
    """Devuelve (action, campos ocultos) del primer <form> que contiene el marcador."""
    for m in re.finditer(r"<form\b([^>]*)>(.*?)</form>", pagina, re.S):
        if marcador in m.group(2):
            accion = html.unescape(re.search(r'action="([^"]+)"', m.group(1)).group(1))
            campos = []
            for entrada in re.findall(r"<input\b[^>]*>", m.group(2)):
                if 'type="hidden"' not in entrada:
                    continue
                nombre = re.search(r'name="([^"]+)"', entrada)
                valor = re.search(r'value="([^"]*)"', entrada)
                if nombre:
                    campos.append((nombre.group(1), html.unescape(valor.group(1)) if valor else ""))
            return accion, campos
    raise SystemExit(f"No se encontró el formulario con «{marcador}».")


def opciones_filemanager(pagina: str) -> dict:
    """Extrae itemid, contexto, límites y el repositorio de subida del filemanager."""
    m = re.search(r'M\.form_filemanager\.init\(Y,\s*(\{.*?\})\);', pagina, re.S)
    if not m:
        raise SystemExit("No se encontró la configuración del filemanager.")
    cfg = json.loads(m.group(1))
    repos = cfg.get("filepicker", {}).get("repositories", {}) or cfg.get("repositories", {})
    subida = [r for r in repos.values() if r.get("type") == "upload"]
    return {
        "itemid": cfg.get("itemid"),
        "client_id": cfg.get("client_id"),
        "ctx_id": (cfg.get("context") or cfg.get("filepicker", {}).get("context") or {}).get("id"),
        "maxfiles": cfg.get("maxfiles"),
        "maxbytes": cfg.get("maxbytes"),
        "repo_id": subida[0]["id"] if subida else None,
        "accepted_types": cfg.get("accepted_types") or cfg.get("filepicker", {}).get("accepted_types"),
    }


def subir(s: Sesion, clave: str, op: dict, archivo: Path, autor: str) -> dict:
    limite = "----moodle" + uuid.uuid4().hex
    campos = {
        "sesskey": clave, "repo_id": str(op["repo_id"]), "itemid": str(op["itemid"]), "ctx_id": str(op["ctx_id"]),
        "savepath": "/", "title": archivo.name, "author": autor, "license": "allrightsreserved",
        "maxbytes": str(op["maxbytes"] if op["maxbytes"] is not None else -1), "areamaxbytes": "-1",
        "client_id": str(op["client_id"] or ""), "env": "filemanager",
    }
    cuerpo = b""
    for k, v in campos.items():
        cuerpo += f"--{limite}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    tipo = mimetypes.guess_type(archivo.name)[0] or "application/octet-stream"
    cuerpo += (f"--{limite}\r\nContent-Disposition: form-data; name=\"repo_upload_file\"; "
               f"filename=\"{archivo.name}\"\r\nContent-Type: {tipo}\r\n\r\n").encode()
    cuerpo += archivo.read_bytes() + f"\r\n--{limite}--\r\n".encode()
    pet = urllib.request.Request(f"{BASE}/repository/repository_ajax.php?action=upload", data=cuerpo)
    pet.add_unredirected_header("Cookie", s.galleta)
    pet.add_header("User-Agent", UA)
    pet.add_header("Content-Type", f"multipart/form-data; boundary={limite}")
    with s._abridor.open(pet, timeout=120) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def estado(s: Sesion, cmid: int) -> dict:
    pagina = s.get("/mod/assign/view.php", id=cmid)
    exigir_sesion(pagina)
    filas = {}
    for rotulo in ("Estado de la entrega", "Estado de la calificación", "Última modificación"):
        m = re.search(re.escape(rotulo) + r"\s*</th>\s*<td[^>]*>(.*?)</td>", pagina, re.S)
        filas[rotulo] = texto(m.group(1)) if m else None
    archivos = sorted(set(html.unescape(n) for n in re.findall(r'/assignsubmission_file/submission_files/\d+/([^"?]+)', pagina)))
    return {"estado": filas.get("Estado de la entrega"), "calificacion": filas.get("Estado de la calificación"),
            "modificado": filas.get("Última modificación"), "archivos": [urllib.parse.unquote(a) for a in archivos],
            "puede_enviar": "action=submit" in pagina or 'value="submit"' in pagina}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cmid", type=int, required=True)
    ap.add_argument("--archivo", action="append", default=[])
    ap.add_argument("--estado", action="store_true")
    ap.add_argument("--simular", action="store_true")
    ap.add_argument("--enviar", action="store_true")
    ap.add_argument("--autor", default="")
    a = ap.parse_args()
    galleta = os.environ.get("MOODLE_COOKIE", "").strip()
    if not galleta:
        raise SystemExit("Falta MOODLE_COOKIE (por ejemplo MoodleSession=...), copiada del navegador con la sesión abierta.")
    s = Sesion(BASE, galleta)

    if a.estado:
        print(json.dumps(estado(s, a.cmid), ensure_ascii=False, indent=1))
        return 0

    if a.enviar:
        pagina = s.get("/mod/assign/view.php", id=a.cmid, action="submit")
        exigir_sesion(pagina)
        accion, campos = formulario(pagina, "confirmsubmit")
        if "submissionstatement" in pagina:
            campos.append(("submissionstatement", "1"))
        campos.append(("submitbutton", "Continuar"))
        s.post(urllib.parse.urlparse(accion).path, campos)
        print(json.dumps(estado(s, a.cmid), ensure_ascii=False, indent=1))
        return 0

    archivos = [Path(x) for x in a.archivo]
    for f in archivos:
        if not f.is_file():
            raise SystemExit(f"No existe {f}")
    pagina = s.get("/mod/assign/view.php", id=a.cmid, action="editsubmission")
    exigir_sesion(pagina)
    clave = sesskey(pagina)
    accion, campos = formulario(pagina, "files_filemanager")
    op = opciones_filemanager(pagina)
    borrador = dict(campos).get("files_filemanager")
    resumen = {"accion": urllib.parse.urlparse(accion).path, "campos": [k for k, _ in campos],
               "itemid_formulario": borrador, "filemanager": {k: v for k, v in op.items() if k != "client_id"},
               "archivos": [(f.name, f.stat().st_size) for f in archivos]}
    if op["maxfiles"] not in (None, -1) and len(archivos) > int(op["maxfiles"]):
        raise SystemExit(f"Demasiados archivos: {len(archivos)} > {op['maxfiles']}")
    if a.simular:
        print(json.dumps(resumen, ensure_ascii=False, indent=1))
        return 0
    for f in archivos:
        r = subir(s, clave, op, f, a.autor)
        if "error" in r:
            raise SystemExit(f"Error al subir {f.name}: {r['error']}")
        print("subido:", f.name)
    campos = [(k, v) for k, v in campos if k != "files_filemanager"] + [("files_filemanager", str(op["itemid"]))]
    campos.append(("submitbutton", "Guardar cambios"))
    s.post(urllib.parse.urlparse(accion).path, campos)
    print(json.dumps(estado(s, a.cmid), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
