# Session 16 — CI/CD with GitHub Actions

This submission extends the supplied `session-16-github-actions/10-final-cicd-pipeline` calculator: the existing five arithmetic tests gate a Docker image build, artifact delivery, and a real Kubernetes deployment on a disposable Kind cluster. The HTTP calculator returns 15 for `10 + 5`. Two replicas have readiness and liveness probes and run as a non-root user.

## Pipeline

`push → CI: checkout → Python → tests → secret check → application/Docker build → upload artifact → CD: download → load image → Kubernetes deployment → HTTP assertion → cluster cleanup`

| Concept | Implementation |
|---|---|
| CI | Tests and builds each change to this branch/project. Failed tests prevent CD. |
| CD | Downloads the built image, deploys two Kubernetes replicas, waits for rollout and verifies HTTP. |
| Workflow | Repository-root `.github/workflows/session16-ci-cd.yml`; push and manual triggers. |
| Jobs | `ci` and `cd`, ordered by `needs: ci`, on separate Ubuntu 24.04 hosted runners. |
| Steps | Checkout, dependency installation, pytest, Docker build/save, artifact transfer, deployment. |
| Runner | A fresh hosted VM for each job; CD needs the image artifact because runners do not share Docker state. |
| Secrets | Random demonstration `SESSION16_DEMO_TOKEN` stored in repository Actions secrets; check only its presence. Its value is never printed or committed. |
| Artifacts | `session16-calculator-build`: application, build information, JUnit XML and compressed Docker image; retained 7 days. |
| Deployment target | Temporary Kind cluster on the runner, deleted at job completion. This demonstrates deployment without a persistent cloud server. |

## Reproduce

```bash
cd session-16-github-actions/session-16-github-actions/10-final-cicd-pipeline
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
bash build.sh
docker build -t session16-calculator:demo .
bash deploy.sh
```

Local deployment requires Docker, Kind and kubectl. GitHub CI installs Kind itself. Push application changes to `session16-github-actions`; inspect the two jobs in Actions. The deployment verifies `/health` and `/calculate?op=add&a=10&b=5`. The original interactive CLI remains available as `python -m app.calculator`.

## References

[GitHub artifact transfer](https://docs.github.com/en/actions/tutorials/store-and-share-data) explains passing a build between jobs. [Kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/) documents loading Docker images into its Kubernetes nodes.

## Execution evidence

Actual run details and Terminal screenshots are added after the workflow completes.
