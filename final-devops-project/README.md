# LabLedger · Final DevOps Capstone

**Session 21 · Shivam Jaiswal · Campus equipment inventory and lending**

[![Capstone CI](https://github.com/shivam24bcs10251-sys/devops-heros/actions/workflows/session21-capstone.yml/badge.svg?branch=session21-final-devops-project)](https://github.com/shivam24bcs10251-sys/devops-heros/actions/workflows/session21-capstone.yml)

LabLedger gives a campus equipment desk a live inventory, checkout records and a reliable return process. This is an original application domain and implementation: a React dashboard, a FastAPI API, PostgreSQL migrations, stock consistency rules and a delivery pipeline that verifies real deployments on two CPU architectures.

> **Execution status:** Application, Docker, CI/security, local Kubernetes/Helm, monitoring, GitOps and the troubleshooting lab have been executed. **The live AWS portion of M7 is pending account permissions.** Terraform validation and two mock plan tests pass, but they are not a live AWS plan, EKS deployment or successful destroy. No AWS resources were created by this project.

![LabLedger running through Kubernetes Ingress](Output/10-ingress-app-browser.png)

*Real browser view of the seeded Kubernetes application. Demo borrowers are synthetic; verification runs later add clearly tagged VERIFY records.*

## Contents

1. [Requirement map](#requirement-map)
2. [Architecture and technologies](#architecture-and-technologies)
3. [Application and tests](#application-and-tests)
4. [Docker quick start](#docker-quick-start)
5. [Kubernetes and Helm](#kubernetes-and-helm)
6. [Terraform infrastructure](#terraform-infrastructure)
7. [CI/CD and DevSecOps](#cicd-and-devsecops)
8. [Monitoring and logs](#monitoring-and-logs)
9. [GitOps and demonstrated release](#gitops-and-demonstrated-release)
10. [Troubleshooting and recovery](#troubleshooting-and-recovery)
11. [Screenshot evidence](#screenshot-evidence)
12. [Lessons learned and operating limits](#lessons-learned-and-operating-limits)
13. [Cleanup](#cleanup)

## Requirement map

| Rubric module | Implementation and actual verification | Status |
|---|---|---|
| M1 · Application | Asset CRUD, borrowing/return API, original React UI, PostgreSQL/Alembic | Executed |
| M2 · Testing | 20 isolated API tests, 91.71% coverage; 6 frontend regression tests; live PostgreSQL concurrency checks | Passed |
| M3 · Git/GitHub | Dedicated branch, more than 10 meaningful commits, tracked lock files, ignored credentials | Executed |
| M4 · Docker | Three healthy Compose services, migration job, multistage frontend, nonroot app images | Executed |
| M5 · CI/CD | GitHub tests/scans → native AMD64/ARM64 builds → GHCR → real Kind/Helm verification → GitOps promotion | Two successful releases |
| M6 · DevSecOps | Bandit, Python/npm SCA, Gitleaks, both-image Trivy HIGH/CRITICAL gates | Passed |
| M7 · Terraform/AWS | VPC/EKS code, provider lock, fmt/validate, two mocked architecture tests | **Live provision/console/destroy pending** |
| M8 · Kubernetes/Helm | Two frontend/backend replicas, Services, ConfigMap, external Secret, Ingress, probes, PVC, HPA | Executed locally |
| M9 · Observability | Two live backend scrape targets, populated six-panel Grafana dashboard, structured request logs | Executed |
| M10 · Documentation | Setup, architecture, linked source/reports/screenshots, four fault investigations and recovery | Documented |

The [assignment](https://docs.google.com/document/d/1cjXFYf2Thm8cBEN-0C48B-v02cj3jGLd47lcO18prHE/edit) and [provided grading rubric](../session21-python/GRADING.md) are the checklist. Cloud execution evidence must be added after an authorized AWS profile is configured; local Kubernetes evidence does not substitute for M7.

## Architecture and technologies

```mermaid
flowchart LR
  User[Equipment desk] --> Ingress[Traefik Ingress]
  Ingress -->|/| UI[React / Nginx · 2 replicas]
  Ingress -->|/api| API[FastAPI · 2–4 replicas]
  UI -->|API calls| API
  API --> DB[(PostgreSQL 17 · StatefulSet)]
  DB --> PVC[(2 GiB persistent volume)]
  Secret[External database Secret] --> API
  Secret --> DB
  Config[ConfigMap / release SHA] --> API
  Job[Alembic migration Job] --> DB
  HPA[Metrics Server / CPU HPA] --> API
  API -->|/metrics| Prom[Prometheus]
  Prom --> Graf[Grafana · 6 live panels]
```

```mermaid
flowchart LR
  Commit[Application Git commit] --> CI[GitHub Actions]
  CI --> Quality[API + frontend tests / SAST / SCA / secrets]
  Quality --> Matrix[Native AMD64 and ARM64 Docker builds]
  Matrix --> Gate[Trivy gates · both images]
  Gate --> GHCR[GHCR · SHA-tagged images]
  GHCR --> Kind[Two isolated Kind / Helm / PostgreSQL checks]
  Kind --> Manifest[Publish multiarch SHA manifests]
  Manifest --> Promote[Bot commits verified tags to Git]
  Promote --> Argo[Argo CD watches branch]
  Argo --> Helm[Helm render / migration sync waves]
  Helm --> Cluster[Kubernetes rolling deployment]
```

The delivered cloud design is VPC → two public subnets/IGW → EKS 1.35 → one managed worker, EBS CSI via Pod Identity and Metrics Server. **That cloud diagram describes Terraform intent; execution remains pending.** The recorded deployment uses the existing `devops-assignment` Minikube cluster, Session 12 Traefik and Session 20 Argo CD. App and monitoring resources are isolated in namespace `session21`.

| Layer | Technologies |
|---|---|
| Application | Python 3.12, FastAPI, SQLAlchemy, Pydantic, Psycopg, Alembic, PostgreSQL 17 |
| Frontend | React 19, Vite 8, Node 24 build stage, unprivileged Nginx |
| Verification | Pytest/pytest-cov, Node test runner, real HTTP/PostgreSQL checks |
| Security | Bandit, pip-audit, npm audit, Gitleaks 8.30.1, Trivy 0.75.0 |
| Delivery | Docker/Compose, GitHub Actions, GHCR AMD64/ARM64 manifests, Kind 0.33, Helm |
| Cluster | Kubernetes 1.35 local, Traefik, Metrics Server, Argo CD 3.5.4 |
| Infrastructure | Terraform, AWS provider 6.67.0, EKS/VPC/EBS Pod Identity |
| Monitoring | Prometheus 3.15.0, Grafana 12.1.1, instrumentator and Linux process metrics |

### Repository layout

```text
final-devops-project/
├── application/              # backend app/tests/migrations and frontend source
├── docker/                   # both Dockerfiles, Nginx, three-service Compose stack
├── kubernetes/               # namespace and cloud-only gp3 StorageClass
├── helm/labledger/           # chart, environment values and all app resources
├── terraform/                # AWS infrastructure, provider lock, mock tests
├── .github/workflows/        # readable copy of the active root workflow
├── security/                 # Trivy gate configuration and security notes
├── monitoring/               # Prometheus/RBAC/rules and provisioned Grafana dashboard
├── gitops/                   # AppProject, Application, promoted image tags
├── scripts/                  # external Secret bootstrap, seed and live verification
├── troubleshooting/          # recovery playbook and bounded read-only load tool
└── Output/                   # real screenshots, Terminal transcripts, scan/test reports
```

GitHub executes [the repository-root workflow](../.github/workflows/session21-capstone.yml). The nested workflow is an identical deliverable copy; GitHub does not discover workflows below the root `.github/workflows/` directory.

## Application and tests

### Business behavior

Assets have a unique tag, category, description, total units and available units. Borrowing decrements availability, returning restores it once, and loan history is retained. PostgreSQL row locks serialize concurrent stock changes. Database constraints prevent negative stock or availability greater than total. Requests that oversubscribe stock, double-return a loan, reduce stock below outstanding loans or remove equipment with lending history return HTTP 409.

| Method | Endpoint | Behavior |
|---|---|---|
| GET/POST | `/api/assets` | List/create equipment |
| GET/PUT/DELETE | `/api/assets/{id}` | Read/edit/delete unused equipment |
| GET/POST | `/api/loans` | List history / borrow available units |
| PUT | `/api/loans/{id}/return` | Return once and restore stock |
| GET | `/api/stats` | Equipment, available units, on-loan units and active loans |
| GET | `/health` | Cheap process liveness and image SHA |
| GET | `/ready` | Database connection and migrated schema readiness |
| GET | `/metrics` | Real HTTP and Linux process metrics |

The frontend supports category, tag/name and **available-to-borrow** filters, add/edit/delete, checkout/return and searchable lending history. Generated demo borrowers are marked `Demo`. The live verification script creates `VERIFY-*` records; historical fixtures remain because the retention rule is intentional.

### Source setup and isolated tests

From the repository root:

```bash
git switch session21-final-devops-project
cd final-devops-project
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r application/backend/requirements-dev.txt
cd application/backend
pytest -v --cov=app --cov-report=term-missing --cov-fail-under=85
cd ../frontend
npm ci
npm test
npm run build
cd ../..
```

On macOS, `uv venv --python 3.12 --seed .venv` is an alternative if the local Python installation cannot run ensurepip. The API tests use a separate in-memory SQLite database through a dependency override, never the live PostgreSQL database. Real PostgreSQL behavior is additionally exercised by `scripts/verify.py`, including two simultaneous attempts to borrow the final unit: exactly one HTTP 201 and one HTTP 409.

The schema is managed by [Alembic migration 0001](application/backend/alembic/versions/0001_inventory.py). Startup does not create production tables. Compose runs a migration service; Kubernetes runs an ordered migration Job before the application release.

## Docker quick start

Requires Docker Desktop/Engine with Compose. Run from `final-devops-project/`:

```bash
python3 scripts/local-env.py
docker compose --env-file .env -f docker/compose.yaml up --build -d
docker compose --env-file .env -f docker/compose.yaml ps -a
python3 scripts/seed.py --base http://127.0.0.1:3021
python3 scripts/verify.py --base http://127.0.0.1:3021
```

Open **http://127.0.0.1:3021**; direct API/docs are on **http://127.0.0.1:8021/docs**. Postgres has no host-exposed port. `local-env.py` generates an ignored mode-0600 `.env` containing a random database password; it preserves an existing environment file. Never paste its content into a screenshot.

Compose starts PostgreSQL, executes Alembic, starts the backend after the migration succeeds and starts the frontend after backend readiness. The migration container exits successfully; the other three services remain healthy. PostgreSQL uses a named persistent volume. Backend runs as UID 10001; the multistage frontend runs as UID 101 and serves on port 8080.

## Kubernetes and Helm

The final chart defines ClusterIP Services `frontend:80`, `backend:8000`, `postgres:5432`; two frontend replicas; a CPU HPA controlling two to four backend replicas; ConfigMap; startup/liveness/readiness probes; ordered migration Job; StatefulSet and a 2 GiB database PVC. The external database Secret is created separately, never embedded in Helm values or Git.

For a fresh local cluster, run from `final-devops-project/`:

```bash
minikube start -p devops-assignment --driver=docker --cpus=2 --memory=3072
minikube -p devops-assignment addons enable metrics-server
kubectl config use-context devops-assignment
python3 scripts/bootstrap.py
helm lint helm/labledger
helm upgrade --install labledger helm/labledger -n session21   -f gitops/values.yaml --wait --timeout 300s
kubectl get deploy,statefulset,pods,svc,ingress,pvc,hpa -n session21
```

The committed GitOps values contain verified GHCR SHA tags. Public images can be pulled anonymously. For local source-image testing, build the Compose images, load them into Minikube and pass `--set backend.image=labledger-backend --set backend.tag=local --set frontend.image=labledger-frontend --set frontend.tag=local` instead of registry values.

Install an ingress controller if one is absent:

```bash
helm repo add traefik https://traefik.github.io/charts
helm upgrade --install session21-ingress traefik/traefik   -n session21-ingress --create-namespace --version 41.6.1
kubectl port-forward -n session21-ingress svc/session21-ingress-traefik 8086:80
```

Open **http://labledger.localhost:8086**. The recorded run reused `session12-ingress-traefik` in namespace `session12-controller`; its forward command uses that name. `/` serves the frontend and `/api` reaches the backend. Alternative access without Ingress:

```bash
kubectl port-forward -n session21 svc/frontend 3121:80
kubectl port-forward -n session21 svc/backend 8121:8000
```

Run each port-forward in a separate terminal. A Service port-forward attaches to a selected Pod; restart it after that Pod is replaced during a rollout.

HPA needs working Metrics Server and declared CPU requests. The bounded, read-only load demonstration is reproducible with `python3 troubleshooting/load.py --workers 12 --seconds 75 --interval 0.05`; inspect `kubectl get hpa` and `kubectl top pods` during the test. Temporary extra Pods can appear during rolling updates because `maxSurge` preserves availability.

## Terraform infrastructure

[Terraform instructions](terraform/README.md) describe the real infrastructure, profile requirements, deployment and verified cleanup procedure. Two public subnets avoid a NAT gateway in this classroom design. EKS API access requires an explicit administrator IPv4 `/32`; unrestricted `0.0.0.0/0` is rejected by validation. There is one managed worker by default, maximum two, with no SSH key or inbound SSH rule. EBS CSI uses a dedicated role through EKS Pod Identity.

```bash
terraform -chdir=terraform init
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform validate
terraform -chdir=terraform test
# After an authorized profile is configured:
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# Edit the profile and current public administrator IPv4/32.
terraform -chdir=terraform plan -out=lab.tfplan
terraform -chdir=terraform apply lab.tfplan
```

**Actual result:** fmt/validate and two mocked plan tests passed. The AWS identity check succeeded, but `aws ec2 describe-vpcs --region ap-south-1` returned `UnauthorizedOperation`. The existing IAM-only account cannot provision this infrastructure. There is consequently no cloud plan/apply/console/destroy screenshot to present as completed.

After AWS access is granted, apply the infrastructure, configure kubectl, apply [the EKS-only gp3 StorageClass](kubernetes/storageclass-eks.yaml), pass `--set postgres.storageClass=labledger-gp3`, configure actual ingress DNS and record AWS resources and destruction. Do not apply that EBS StorageClass to Minikube. Cloud costs depend on resource lifetime; no cost cap or free-tier eligibility is claimed.

## CI/CD and DevSecOps

[Successful first release](https://github.com/shivam24bcs10251-sys/devops-heros/actions/runs/37619323230) · [Successful feature release](https://github.com/shivam24bcs10251-sys/devops-heros/actions/runs/37620612050)

1. API tests must pass at least 85% coverage; frontend regression tests/build must pass.
2. Bandit SAST, Python dependency audit, npm audit and redacted Gitleaks secret scans block failures.
3. Native AMD64 and ARM64 jobs build both runtime images from the same application SHA.
4. Trivy examines both images and blocks **all HIGH/CRITICAL findings**, including findings without a fix. There is no CVE allowlist or bypass.
5. Images are published with `${commit}-${architecture}` tags. Each architecture creates its own isolated Kind cluster, installs the Helm chart with two frontend/two backend replicas and PostgreSQL, and executes real business-rule/concurrency checks.
6. Only after both deployment jobs pass are the multiarchitecture `${commit}` manifests published and verified image tags committed to GitOps values.
7. Argo CD reconciles that commit into the local cluster. CI never needs the workstation kubeconfig or AWS credentials.

Pushes to `main` and this session branch run the pipeline for relevant source paths. Pull requests to `main` run quality/security checks without registry publishing; manual dispatch is also available. This capstone's promotion target is the session branch; merging it to main requires updating the GitOps target/promotion policy deliberately. Documentation-only pushes do not rebuild unchanged application images. Bot promotions use `[skip ci]` and do not create a workflow loop.

| Gate | Recorded result |
|---|---|
| Pytest | 20 passed; 91.71% coverage |
| Frontend regression tests | 6 passed |
| Bandit | Zero findings |
| pip-audit / npm audit | No known runtime dependency vulnerabilities in the scan snapshot |
| Gitleaks | No committed source secrets detected |
| Trivy backend + frontend, AMD64 + ARM64 | Zero HIGH/CRITICAL findings in all four CI reports |
| Kubernetes deployment checks | Passed on both native architectures |

See [security details](security/README.md), [machine-readable scan summary](Output/reports/security-summary.json) and [CI reports and normalization notes](Output/reports/README.md). Reports record the scanner/database snapshot; zero known findings are not a guarantee of future safety. Two legacy repository gitlinks lack entries in the provided `.gitmodules`, producing checkout post-cleanup warnings; all capstone quality, scan, publish and deployment steps still completed successfully. The existing reference files were preserved.

The local secret scan archives committed source so ignored local credentials are excluded rather than suppressed through an allowlist.

Image names are `ghcr.io/shivam24bcs10251-sys/labledger-backend` and `ghcr.io/shivam24bcs10251-sys/labledger-frontend`. [Backend package](https://github.com/users/shivam24bcs10251-sys/packages/container/package/labledger-backend) · [Frontend package](https://github.com/users/shivam24bcs10251-sys/packages/container/package/labledger-frontend). Final demonstrated application SHA: **`9faeab4771c5eaddc22d8b201415fc20b33476cf`**. Both SHA manifests contain `linux/amd64` and `linux/arm64` variants.

## Monitoring and logs

```bash
kubectl apply -f monitoring/
kubectl rollout status deploy/session21-prometheus -n session21
kubectl rollout status deploy/session21-grafana -n session21
kubectl port-forward -n session21 svc/session21-prometheus 9091:9090
kubectl port-forward -n session21 svc/session21-grafana 3005:3000
```

Open **http://127.0.0.1:9091/targets** and **http://127.0.0.1:3005/d/labledger**. Prometheus discovers each backend Pod with namespace-scoped RBAC. Grafana automatically provisions the real datasource and dashboard: request throughput, backend scrape targets UP, p95 latency, requests by handler, process RSS and CPU percent of one core. Resource metrics used by HPA come separately from Metrics Server.

Each backend request emits structured JSON containing method, path, HTTP status, duration, request ID and release SHA. The evidence includes a request tagged `session21-evidence`; that ID joins a command to its real log entry. No distributed tracing export is claimed.

Prometheus contains unavailable-target and sustained 5xx-ratio rules. There is no external alert notification receiver. Grafana anonymous access is Viewer-only for the local lab. Monitoring history uses `emptyDir`; persistent database storage does not imply persistent monitoring history. See [monitoring notes](monitoring/README.md).

## GitOps and demonstrated release

The [AppProject](gitops/project.yaml) restricts source repository, destination namespace and allowed resource kinds. The [Application](gitops/application.yaml) uses the Helm chart and promoted values from the same branch through two source references. Automated reconciliation enables prune and self-heal. Database credentials remain an external Secret.

For a fresh Argo CD installation:

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm upgrade --install session20-argocd argo/argo-cd   -n session20-argocd --create-namespace --version 10.9.7   -f gitops/argocd-values.yaml
kubectl apply -f gitops/project.yaml -f gitops/application.yaml
kubectl port-forward -n session20-argocd svc/session20-argocd-server 8083:80
```

Open **http://127.0.0.1:8083** and authenticate using the local Argo CD administrator secret without including it in evidence. The installation name matches the existing Session 20 controller reused in the recorded run. Once Argo CD adopts the release, it renders Helm and owns the live resources; the earlier Helm history is the bootstrap record and does not track later GitOps deployments.

| Release stage | Actual commit / result |
|---|---|
| First tested application release | `22e7cbd8787485dae798a10532d59c6d19f3882b`, successful CI, deployed by Argo CD |
| Meaningful feature change | `9faeab4771c5eaddc22d8b201415fc20b33476cf`, available-only inventory filter and searchable history, six regression tests |
| Verified tag promotion | Bot commit `03fbb01` updates both `gitops/values.yaml` tags after both architecture jobs pass |
| Reconciliation | Migration Job → rolling frontend/backend update → SHA verified through `/health` → Synced/Healthy |

Sync waves create DB/config at wave 0, run the one-shot Alembic Job at wave 1, deploy application/services at wave 2 and configure Ingress/HPA at wave 3. Init containers wait for the schema. The deployment omits fixed backend replicas while HPA is enabled, preventing Argo CD from fighting the autoscaler.

During deliberate fault investigation, automated sync was temporarily paused so self-healing would not hide the failure. The committed policy was restored afterward. Final screenshots show the recovered, reconciled application and updated source SHA.

## Troubleshooting and recovery

[Detailed fault playbook](troubleshooting/README.md) records symptoms, investigation, root cause, exact commands, fix and verification. All faults were introduced in namespace `session21`; the PVC and other sessions were preserved.

| Fault | Observed evidence | Root cause / repair | Verification |
|---|---|---|---|
| Invalid backend image tag | New Pod cannot pull image; old replicas still serve | Nonexistent GHCR tag; restore verified SHA | Rollout completes, API returns release SHA |
| Wrong Service selector | Empty backend endpoints, HTTP 503 | Selector does not match Pod labels; restore `app=labledger-backend` | EndpointSlice repopulates, HTTP 200 |
| Route to closed port | Valid Service/Ingress route on 8080 returns HTTP 502 | Backend listens on 8000; restore route and remove injected port | HTTP 200 |
| PostgreSQL unavailable | `/health` 200, `/ready` 503 | DB StatefulSet scaled to zero; restore one replica | `/ready` 200; same stock/loan counts and same bound PVC |

A nonexistent Ingress Service port initially produced a controller `service port not found` error while Traefik retained its last valid route. Checking only HTTP status would have missed this defect. The closed-port test then demonstrated an actual traffic failure and recovery.

## Screenshot evidence

Every image below is a real OS screenshot of the actual Terminal/browser window, with no surrounding desktop. Capture commands run in a separate helper window and do not appear in the Terminal evidence. Commands and full output are preserved in the adjacent text transcripts. Browser screenshots show real running pages; there are no simulated pipeline results, cloud screenshots or fabricated monitoring values.


<details>
<summary><strong>Application, tests, Docker and infrastructure</strong></summary>

### 01 · Project and branch

![Project and branch](Output/01-project-and-branch.png)

[Commands and actual output](Output/logs/01-project-and-branch.txt).

### 02 · Api tests

![Api tests](Output/02-api-tests.png)

[Commands and actual output](Output/logs/02-api-tests.txt).

### 03 · Frontend build

![Frontend build](Output/03-frontend-build.png)

[Commands and actual output](Output/logs/03-frontend-build.txt).

### 04 · Security source

![Security source](Output/04-security-source.png)

[Commands and actual output](Output/logs/04-security-source.txt).

### 05 · Compose running

![Compose running](Output/05-compose-running.png)

[Commands and actual output](Output/logs/05-compose-running.txt).

### 06 · Compose business

![Compose business](Output/06-compose-business.png)

[Commands and actual output](Output/logs/06-compose-business.txt).

### 07 · Terraform validation

![Terraform validation](Output/07-terraform-validation.png)

[Commands and actual output](Output/logs/07-terraform-validation.txt).

### 08 · Aws access pending

![Aws access pending](Output/08-aws-access-pending.png)

[Commands and actual output](Output/logs/08-aws-access-pending.txt).

### 09 · Compose app browser

![Compose app browser](Output/09-compose-app-browser.png)

### 10 · Ingress app browser

![Ingress app browser](Output/10-ingress-app-browser.png)

</details>

<details>
<summary><strong>Kubernetes, monitoring and initial GitOps release</strong></summary>

### 11 · Helm and kubernetes

![Helm and kubernetes](Output/11-helm-and-kubernetes.png)

[Commands and actual output](Output/logs/11-helm-and-kubernetes.txt).

### 12 · Config secret storage

![Config secret storage](Output/12-config-secret-storage.png)

[Commands and actual output](Output/logs/12-config-secret-storage.txt).

### 13 · Api metrics

![Api metrics](Output/13-api-metrics.png)

[Commands and actual output](Output/logs/13-api-metrics.txt).

### 14 · Live api and database

![Live api and database](Output/14-live-api-and-database.png)

[Commands and actual output](Output/logs/14-live-api-and-database.txt).

### 15 · Prometheus targets browser

![Prometheus targets browser](Output/15-prometheus-targets-browser.png)

### 16 · Grafana dashboard browser

![Grafana dashboard browser](Output/16-grafana-dashboard-browser.png)

### 17 · Gitops initial browser

![Gitops initial browser](Output/17-gitops-initial-browser.png)

### 18 · Gitops before release

![Gitops before release](Output/18-gitops-before-release.png)

[Commands and actual output](Output/logs/18-gitops-before-release.txt).

</details>

<details>
<summary><strong>Deliberate failures and recovery</strong></summary>

### 19 · Fault image

![Fault image](Output/19-fault-image.png)

[Commands and actual output](Output/logs/19-fault-image.txt).

### 20 · Fix image

![Fix image](Output/20-fix-image.png)

[Commands and actual output](Output/logs/20-fix-image.txt).

### 21 · Fault service

![Fault service](Output/21-fault-service.png)

[Commands and actual output](Output/logs/21-fault-service.txt).

### 22 · Fix service

![Fix service](Output/22-fix-service.png)

[Commands and actual output](Output/logs/22-fix-service.txt).

### 23 · Fault ingress

![Fault ingress](Output/23-fault-ingress.png)

[Commands and actual output](Output/logs/23-fault-ingress.txt).

### 24 · Fix ingress

![Fix ingress](Output/24-fix-ingress.png)

[Commands and actual output](Output/logs/24-fix-ingress.txt).

### 25 · Fault database

![Fault database](Output/25-fault-database.png)

[Commands and actual output](Output/logs/25-fault-database.txt).

### 26 · Fix database

![Fix database](Output/26-fix-database.png)

[Commands and actual output](Output/logs/26-fix-database.txt).

### 27 · Request logs

![Request logs](Output/27-request-logs.png)

[Commands and actual output](Output/logs/27-request-logs.txt).

</details>

<details>
<summary><strong>CI, registry, autoscaling and final release</strong></summary>

### 28 · Ci green browser

![Ci green browser](Output/28-ci-green-browser.png)

### 29 · Hpa under load

![Hpa under load](Output/29-hpa-under-load.png)

[Commands and actual output](Output/logs/29-hpa-under-load.txt).

### 30 · Ghcr backend browser

![Ghcr backend browser](Output/30-ghcr-backend-browser.png)

### 31 · Ghcr frontend browser

![Ghcr frontend browser](Output/31-ghcr-frontend-browser.png)

### 32 · Ci security deployment browser

![Ci security deployment browser](Output/32-ci-security-deployment-browser.png)

### 33 · Hpa healthy load

![Hpa healthy load](Output/33-hpa-healthy-load.png)

[Commands and actual output](Output/logs/33-hpa-healthy-load.txt).

### 34 · Hpa recovered

![Hpa recovered](Output/34-hpa-recovered.png)

[Commands and actual output](Output/logs/34-hpa-recovered.txt).

### 35 · Release verification

![Release verification](Output/35-release-verification.png)

[Commands and actual output](Output/logs/35-release-verification.txt).

### 36 · Gitops final browser

![Gitops final browser](Output/36-gitops-final-browser.png)

### 37 · Updated app browser

![Updated app browser](Output/37-updated-app-browser.png)

### 38 · Commit history

![Commit history](Output/38-commit-history.png)

[Commands and actual output](Output/logs/38-commit-history.txt).

### 39 · Trivy and registry

![Trivy and registry](Output/39-trivy-and-registry.png)

[Commands and actual output](Output/logs/39-trivy-and-registry.txt).

### 40 · Frontend regressions

![Frontend regressions](Output/40-frontend-regressions.png)

[Commands and actual output](Output/logs/40-frontend-regressions.txt).

### 41 · Api test cases

![Api test cases](Output/41-api-test-cases.png)

[Commands and actual output](Output/logs/41-api-test-cases.txt).

</details>

## Lessons learned and operating limits

- PostgreSQL row locks and database constraints protect shared inventory; isolated unit tests are complemented by real concurrency checks in both CI deployments.
- Migration ordering matters. A single Job and schema-waiting init containers avoid simultaneous schema changes across replicas.
- Liveness and readiness serve different purposes: a database outage should remove an API Pod from serving traffic without restarting a healthy process repeatedly.
- Service selectors, listening ports and controller logs must agree. A cached valid ingress route can conceal a rejected configuration.
- GitOps image promotion follows successful deployment verification. SHA tags connect an application commit, registry release, migration, live image and request log.
- HPA can scale successfully while a shared local node experiences pressure. The initial load/rollout errors are retained; later throttled runs completed with zero errors.
- An AWS identity check does not establish provisioning permission. Terraform mocks validate configuration logic but cannot prove cloud resources exist.

This is a classroom lab using synthetic data and local HTTP. Authentication/authorization, TLS, managed database backups, image signing/digest promotion, durable monitoring retention and external alert notifications remain production improvements. A TestClient dependency deprecation warning is recorded in the test transcript; it does not fail the 20-test suite. Existing reference-repository gitlinks also produce GitHub checkout cleanup warnings, documented above.

## Cleanup

The running local application is retained for review. To stop Compose while preserving database records:

```bash
docker compose --env-file .env -f docker/compose.yaml down
```

Add `--volumes` only when you intend to delete that lab database. For Kubernetes, first remove the Argo CD Application so it cannot recreate deleted resources, then delete the capstone namespace only when evaluation is finished:

```bash
kubectl delete application labledger -n session20-argocd
kubectl delete appproject session21 -n session20-argocd
kubectl delete namespace session21
```

Deleting namespace `session21` deletes its database PVC. Preserve/export any required records first. Do not delete the shared Minikube cluster, Session 12 ingress controller or Session 20 Argo CD installation to clean up this project. Future AWS destruction must follow the [Terraform teardown procedure](terraform/README.md) and record successful resource removal; no cloud cleanup is claimed for resources that were never created.
