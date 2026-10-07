"""Summarize actual scanner JSON reports without running or bypassing gates."""
import json
from pathlib import Path
import sys

folder = Path(sys.argv[1])
for filename in ['bandit.json', 'pip-audit.json', 'gitleaks.json', 'trivy.json']:
    path = folder / filename
    if not path.exists():
        continue
    data = json.loads(path.read_text())
    if filename == 'bandit.json':
        findings = data.get('results', [])
        blocking = [item for item in findings if item['issue_severity'] in ['MEDIUM', 'HIGH']]
        print(f'Bandit: {len(findings)} findings; {len(blocking)} medium/high findings.')
    elif filename == 'pip-audit.json':
        dependencies = data.get('dependencies', [])
        print(f'pip-audit: {len(dependencies)} dependencies; {sum(len(item.get("vulns", [])) for item in dependencies)} known vulnerabilities.')
    elif filename == 'gitleaks.json':
        print(f'Gitleaks: {len(data)} detected secrets (redacted report).')
    else:
        findings = [item for result in data.get('Results', []) for item in result.get('Vulnerabilities', [])]
        blocking = [item for item in findings if item['Severity'] in ['HIGH', 'CRITICAL'] and item.get('FixedVersion')]
        print(f'Trivy report: {len(findings)} findings; {len(blocking)} fixable HIGH/CRITICAL findings.')
        for item in blocking[:8]:
            print(f"  {item['PkgName']}: {item['VulnerabilityID']} {item['InstalledVersion']} -> {item['FixedVersion']}")
