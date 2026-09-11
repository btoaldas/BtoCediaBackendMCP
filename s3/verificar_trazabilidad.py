"""Verifica prospectividad, pedidos literales y fidelidad de los snapshots."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent
EV = BASE / "evidencia/p02"
names = ["01-contrasenas", "02-email", "03-usuarios", "04-administradores"]
prompts = [
    "hazme un validador de contraseñas",
    "agrégale que también valide un formato de email",
    "ahora que maneje una lista de varios usuarios, cada uno con su contraseña y su email",
    "ahora que la validación de contraseña sea opcional para usuarios administradores",
]
hashes = {}
manifest = json.loads((EV / "publicable/rondas-trazabilidad.json").read_text())
assert manifest["version"] == 1 and len(manifest["rondas"]) == 4
for number, (name, expected) in enumerate(zip(names, prompts), start=1):
    prediction = json.loads((EV / f"prediccion-{number:02}.json").read_text())
    stem = "agy-ronda-01-retry" if number == 1 else f"agy-ronda-{number:02}"
    metadata = manifest["rondas"][number - 1]
    assert metadata["ronda"] == number and metadata["prompt"] == expected
    assert prediction["prompt"] == expected
    actual_prompt = (EV / f"prompt-{number:02}-ejecutado.txt").read_text()
    assert actual_prompt.splitlines()[0] == expected
    assert prediction["recorded_at_utc"] == metadata["prediccion_utc"]
    assert datetime.fromisoformat(prediction["recorded_at_utc"]) < datetime.fromisoformat(metadata["generacion_inicio_utc"])
    assert datetime.fromisoformat(metadata["generacion_inicio_utc"]) < datetime.fromisoformat(metadata["generacion_fin_utc"])
    assert metadata["exit_code_agy"] == 0
    response = (EV / f"{stem}.stdout.md").read_text()
    assert metadata["respuesta_archivo"] == f"{stem}.stdout.md"
    assert hashlib.sha256(response.encode()).hexdigest() == metadata["respuesta_sha256"]
    blocks = re.findall(r"```python\n(.*?)```", response, flags=re.S)
    assert len(blocks) == 1
    code = (BASE / "s3/rondas" / name / "main.py").read_text()
    assert code == blocks[0], f"Snapshot {name} alterado respecto de agy"
    compile(code, name + "/main.py", "exec")
    digest = hashlib.sha256(code.encode()).hexdigest()
    assert metadata["codigo"] == f"s3/rondas/{name}/main.py"
    assert digest == metadata["codigo_sha256"]
    hashes[number] = digest
    if number > 1:
        assert (BASE / "s3/rondas" / names[number - 2] / "main.py").read_text() in actual_prompt
    print(json.dumps({"ronda": number, "prediccion_previa": True,
                      "pedido_literal": True, "codigo_identico_a_respuesta_agy": True,
                      "sha256": digest}, ensure_ascii=False))
print("4 rondas trazables: predicciones previas, código exacto y evolución enlazada.")
print("Verificación contra manifiesto publicable; originales de sesión conservados localmente.")
