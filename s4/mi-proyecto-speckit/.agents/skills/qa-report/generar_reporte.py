"""Reporte determinista de la guía con fallos cerrados y salidas HTML escapadas."""
from datetime import datetime, timezone
import html
import json
import re
import subprocess
import sys
from pathlib import Path

UMBRAL_COBERTURA = 50.0
PATRONES_SECRETOS = [r'''(?i)(api[_-]?key|secret|password|token)\s*=\s*['"][^'"]{6,}['"]''']


def correr_tests():
    run = Path('.qa-runs') / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    run.mkdir(parents=True)
    report_path, coverage_path = run / 'tests.json', run / 'coverage.json'
    process = subprocess.run([
        'uv', 'run', 'pytest', '--json-report', f'--json-report-file={report_path}',
        '--cov=src', f'--cov-report=json:{coverage_path}', '-q',
    ], capture_output=True, text=True, timeout=120)
    (run / 'pytest.log').write_text(process.stdout + process.stderr)
    try:
        report = json.loads(report_path.read_text())
        coverage = json.loads(coverage_path.read_text())
    except (OSError, json.JSONDecodeError):
        report, coverage = {}, {}
    summary = report.get('summary', {})
    return {'pasaron': summary.get('passed', 0), 'fallaron': summary.get('failed', 0),
            'errores': summary.get('error', 0), 'total': summary.get('total', 0),
            'exit_code': process.returncode,
            'cobertura_pct': round(coverage.get('totals', {}).get('percent_covered', 0.0), 1),
            'evidencia': str(run)}


def buscar_secretos():
    findings = []
    for path in sorted(Path('src').rglob('*.py')):
        text = path.read_text()
        for pattern in PATRONES_SECRETOS:
            for match in re.finditer(pattern, text):
                line = text.count('\n', 0, match.start()) + 1
                findings.append(f'{path}:{line}: posible literal sensible (valor omitido)')
    return findings


def revisar_higiene_secretos():
    # Git evalúa reglas incluso si .env todavía no existe. No confiar en texto.
    ignored = subprocess.run(['git', 'check-ignore', '--no-index', '-q', '.env'], capture_output=True)
    tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', '.env'], capture_output=True)
    return {'env_example': Path('.env.example').is_file(), 'env_existe': Path('.env').exists(),
            'env_tracked': tracked.returncode == 0, 'gitignore_ok': ignored.returncode == 0}


def construir_html(tests, secretos, higiene):
    aprobado = (tests['exit_code'] == 0 and tests['total'] > 0 and tests['fallaron'] == 0
                and tests['errores'] == 0 and tests['cobertura_pct'] >= UMBRAL_COBERTURA
                and not secretos and higiene['env_example'] and higiene['gitignore_ok']
                and not higiene['env_tracked'])
    verdict = 'APROBADO' if aprobado else 'REQUIERE CORRECCIÓN'
    color = '#176b41' if aprobado else '#aa3025'
    findings = ''.join(f'<li>{html.escape(item)}</li>' for item in secretos) or '<li>Sin hallazgos del patrón automatizado</li>'
    output = f'''<!doctype html><html lang="es"><meta charset="utf-8">
<title>Reporte QA — Conversor de temperatura</title>
<style>body{{font:18px system-ui;margin:50px auto;max-width:900px;line-height:1.55;color:#213143;background:#f5f8fb}}main{{background:white;padding:40px;border:1px solid #dae2eb;border-radius:12px}}h1{{color:{color};margin-top:0}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #dae2eb;padding:10px;text-align:left}}code{{font-size:14px}}small{{color:#52627a}}</style>
<main><small>PRÁCTICA 4 · LABORATORIO PYTHON · REPORTE DETERMINISTA</small>
<h1>{verdict}</h1><p>Conversor de temperatura C / F / K</p>
<table><tr><th>Pruebas reales</th><td>{tests['pasaron']} pasaron · {tests['fallaron']} fallaron · {tests['errores']} errores · {tests['total']} total</td></tr>
<tr><th>Salida de pytest</th><td>{tests['exit_code']}</td></tr>
<tr><th>Cobertura</th><td>{tests['cobertura_pct']}% · umbral {UMBRAL_COBERTURA}%</td></tr>
<tr><th>.env.example</th><td>{higiene['env_example']}</td></tr>
<tr><th>.env ignorado según Git</th><td>{higiene['gitignore_ok']}</td></tr>
<tr><th>.env trackeado</th><td>{higiene['env_tracked']}</td></tr></table>
<h2>Secretos expuestos</h2><ul>{findings}</ul>
<h2>Trazabilidad</h2><p>Spec fuente: <code>specs/001-conversor-temperatura/spec.md</code>.</p>
<p>Evidencia de esta corrida: <code>{html.escape(tests['evidencia'])}</code>.</p>
<p>El veredicto exige exit 0, pruebas recolectadas, 0 fallos, cobertura ≥50%, patrón de secretos sin hallazgos e higiene comprobada con Git. La revisión manual adicional vive en hallazgos-seguridad.md. No es una certificación de seguridad.</p>
<small>Generado {datetime.now(timezone.utc).isoformat()} · sin servicios de IA para redactar el HTML</small></main></html>'''
    # Cada corrida guarda una copia inmutable, además del entregable vigente.
    Path(tests['evidencia'], 'reporte-qa.html').write_text(output)
    final = Path('reporte-qa.html')
    if final.exists():
        Path(tests['evidencia'], 'reporte-qa-anterior.html').write_bytes(final.read_bytes())
    final.write_text(output)
    Path(tests['evidencia'], 'resumen.json').write_text(json.dumps({'veredicto': verdict, 'tests': tests, 'secretos': secretos, 'higiene': higiene}, indent=2, ensure_ascii=False))
    print(verdict)
    print(json.dumps(tests, ensure_ascii=False))
    return aprobado


if __name__ == '__main__':
    sys.exit(0 if construir_html(correr_tests(), buscar_secretos(), revisar_higiene_secretos()) else 1)
