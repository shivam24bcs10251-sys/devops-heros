"""Exercise the SAST gate against a temporary copy of the application."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

source = Path(__file__).resolve().parent.parent / 'demo/app/app.py'
with tempfile.TemporaryDirectory(prefix='session17-security-gate-') as temporary:
    candidate = Path(temporary) / 'app.py'
    candidate.write_text(source.read_text().replace('debug=False', 'debug=True'))
    command = [sys.executable, '-m', 'bandit', '-q', '-ll', '-f', 'json', str(candidate)]
    print('Temporary copy: enable the Flask debugger to test the security gate.', flush=True)
    result = subprocess.run(command, capture_output=True, text=True)
    report = json.loads(result.stdout)
    for issue in report["results"]:
        print(f"{issue['test_id']}: {issue['issue_text']} Severity={issue['issue_severity']} line={issue['line_number']}", flush=True)
    assert result.returncode == 1, 'The SAST gate must reject debug mode.'
    print('Gate rejected the unsafe debugger. Restore debug=False.', flush=True)
    candidate.write_text(source.read_text())
    subprocess.run(command, check=True, capture_output=True, text=True)
    print('SAST gate passed after the fix. Repository application was unchanged.', flush=True)
