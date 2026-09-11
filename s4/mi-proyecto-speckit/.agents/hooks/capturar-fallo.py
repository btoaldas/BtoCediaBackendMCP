"""Conserva fuentes y pruebas del estado que hizo fallar un hook."""
from pathlib import Path
import hashlib
import json
import sys

project=Path.cwd()
target=Path(sys.argv[1])/'estado-fallido'
target.mkdir(exist_ok=False)
paths=[]
for folder,pattern in [('src','*.py'),('tests','*.py'),('specs','spec.md')]:
 paths.extend((project/folder).rglob(pattern))
for name in ['pyproject.toml','.python-version','uv.lock']:
 if (project/name).is_file():paths.append(project/name)
rows={}
for source in paths:
 relative=source.relative_to(project)
 dest=target/relative
 dest.parent.mkdir(parents=True,exist_ok=True)
 data=source.read_bytes()
 with dest.open('xb') as file:file.write(data)
 rows[str(relative)]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
(target/'fuentes-sha256.json').write_text(json.dumps(rows,indent=2))
