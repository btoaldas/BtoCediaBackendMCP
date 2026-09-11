"""Invoca agy real, exige predicción previa y conserva respuesta sin editar."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent.parent
EV = BASE / "evidencia/p02"
round_number = int(sys.argv[1])
prior = {2: "01-contrasenas", 3: "02-email", 4: "03-usuarios"}[round_number]
target = {2: "02-email", 3: "03-usuarios", 4: "04-administradores"}[round_number]
prediction = json.loads((EV / f"prediccion-{round_number:02}.json").read_text())
started = datetime.now(timezone.utc)
assert datetime.fromisoformat(prediction["recorded_at_utc"]) < started
source = (BASE / "s3/rondas" / prior / "main.py").read_text()
prompt = prediction["prompt"] + (
    "\n\nNota operativa del entorno: no uses herramientas, no leas archivos, "
    "no escribas archivos y no ejecutes comandos. Devuelve el código Python "
    "completo en tu respuesta; el operador lo guardará y ejecutará.\n\n"
    "Código de la ronda anterior sobre el cual aplicar el pedido:\n```python\n"
    + source + "```"
)
with (EV / f"prompt-{round_number:02}-ejecutado.txt").open("x") as handle:
    handle.write(prompt)
agy_binary = shutil.which("agy")
assert agy_binary, "No se encontró agy en PATH"
command = [agy_binary, "--sandbox", "--print-timeout", "5m",
           "--log-file", str(EV / f"agy-ronda-{round_number:02}-provider.log"),
           "--print", prompt]
result = subprocess.run(command, cwd=BASE / "s3/experimento", text=True,
                        capture_output=True, timeout=335)
for suffix, content in [("stdout.md", result.stdout), ("stderr.txt", result.stderr)]:
    with (EV / f"agy-ronda-{round_number:02}.{suffix}").open("x") as handle:
        handle.write(content)
meta = {"ronda": round_number, "started_at_utc": started.isoformat(),
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "exit_code": result.returncode,
        "prompt_file": f"prompt-{round_number:02}-ejecutado.txt",
        "prior_code_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "transport": "agy --sandbox --print-timeout 5m --print; no tools"}
with (EV / f"agy-ronda-{round_number:02}.meta.json").open("x") as handle:
    json.dump(meta, handle, ensure_ascii=False, indent=2)
print(json.dumps(meta, ensure_ascii=False))
print(result.stdout)
print(result.stderr)
assert result.returncode == 0 and result.stdout.strip(), "Sin respuesta útil de agy"
blocks = re.findall(r"```python\n(.*?)```", result.stdout, flags=re.S)
assert len(blocks) == 1, "Revisar manualmente: no hay un único bloque Python"
destination = BASE / "s3/rondas" / target
destination.mkdir()
with (destination / "main.py").open("x") as handle:
    handle.write(blocks[0])
