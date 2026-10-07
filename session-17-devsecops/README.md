# Session 17 — Complete CI/CD and DevSecOps

The supplied Flask dashboard is built, tested, scanned, containerized, published to GHCR and deployed to a real disposable Kubernetes cluster by GitHub Actions. The existing dashboard and eight unit tests are retained. Debug mode is disabled, Gunicorn serves the container, and both Kubernetes replicas run without root privileges and have health probes.

## Execution flow

`Code → application build → unit tests → SAST → SCA → secret scan → Docker build → image scan/security gate → registry push → Kubernetes deployment → rollout and HTTP verification`

[Active workflow](../.github/workflows/session17-devsecops.yml) runs on changes to the demo on `session17-devsecops`. The supplied nested workflow is updated for reference; GitHub discovers only the repository-root workflow. A single Ubuntu 24.04 runner retains the exact image between build, scan, push and deployment. Each step must pass before the next runs. Security reports upload even on failure.

| Requirement | Implementation and gate |
|---|---|
| Application build | Install pinned dependencies; compile application Python. |
| Unit tests | Pytest and coverage; any failed test stops delivery. |
| SAST | Bandit scans `demo/app`; medium/high severity findings fail. |
| SCA | pip-audit scans every locked runtime dependency; known vulnerabilities fail. |
| Secrets | Gitleaks default rules scan demo source, tests, config, manifests and active workflow; findings are redacted and fail. This scope excludes other sessions and prior Git history. |
| Docker build | Non-root Python/Gunicorn image built once and tagged with the full Git SHA. |
| Image scan | Trivy blocks fixable HIGH/CRITICAL findings; the complete policy is in [SECURITY.md](demo/SECURITY.md). |
| Registry | `ghcr.io/shivam24bcs10251-sys/devops-heros-session17:<git-sha>`; authenticated using the short-lived Actions token. |
| Kubernetes | Two replicas, probes, resource requests/limits, Service; Kind loads the exact built/published image. |
| Verification | Wait for successful rollout, show image IDs, assert healthy status and addition result 30 over HTTP. |
| Cleanup | Kind cluster is deleted at deployment completion. No persistent cloud resources are created. |

## Local reproduction

```bash
cd session-17-devsecops/demo
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -v --cov=app
bandit -r app -c security/bandit.yaml -ll
pip-audit -r requirements.txt
gitleaks dir . --config security/gitleaks.toml --redact --exit-code 1
export IMAGE=session17-dashboard:local
docker build -t "$IMAGE" .
trivy image --config security/trivy.yaml "$IMAGE"
bash deploy.sh
```

Docker, Kind, kubectl, Gitleaks and Trivy are prerequisites for local deployment. GitHub installs the tools automatically. Runtime dependencies and scanner/test tools are pinned separately. Publishing in CI uses `contents: read` and `packages: write` permissions and no personal token. The registry can be private; the disposable cluster loads the same image directly, so it does not require a stored image-pull secret.

The dashboard's `/api/pipeline/run` endpoint remains a UI simulation. Successful pipeline evidence below comes from the real GitHub runner.

## References

[Gitleaks CLI](https://github.com/gitleaks/gitleaks), [Trivy vulnerability filtering](https://trivy.dev/docs/latest/configuration/filtering/), [GitHub Container Registry authentication](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry), and [Kind image loading](https://kind.sigs.k8s.io/docs/user/quick-start/).

## Container gate investigation

The [first run](https://github.com/shivam24bcs10251-sys/devops-heros/actions/runs/37594603923) stopped at the image scan and skipped publishing/deployment. Its [Trivy report](Output/first-run/trivy.json) identified fixable vulnerabilities in `setuptools` and in `msgpack`/`urllib3` bundled with pip. These package installers are not needed by the running dashboard, so the Dockerfile removes pip/setuptools after installing the pinned application dependencies. The initial YAML also placed `ignore-unfixed` at the wrong level; the corrected `vulnerability.ignore-unfixed` setting enforces the stated fixable HIGH/CRITICAL policy. No CVE-specific exceptions were added.

The [second run](https://github.com/shivam24bcs10251-sys/devops-heros/actions/runs/37594892602) passed all security gates, published the image, and verified two Ready replicas plus the healthy/addition APIs. The HTML preview used `curl | head`, which closed the pipe early and produced a curl write error under `pipefail`. The deployment script now downloads the page to a file before printing its first 250 bytes. [Second-run deployment evidence](Output/second-run/deployment.txt) records the completed API checks before that preview failure.

## Run evidence

Actual successful run, reports, registry digest and screenshots are added after execution.
