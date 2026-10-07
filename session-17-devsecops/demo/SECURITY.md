# Security gates for this classroom demo

Bandit scans application Python and blocks medium/high severity findings. pip-audit audits all locked runtime requirements and blocks any known dependency vulnerability. Gitleaks scans the supplied demo project and the active root workflow using default rules, redacts findings, and blocks detected secrets. Trivy scans the single built image and blocks HIGH/CRITICAL vulnerabilities with an available fix; unresolved findings outside that policy are not a claim of zero risk.

Scans fail the job; registry push and deployment follow only when every gate succeeds. Tool failures also fail the job. No `continue-on-error` or scanner-error suppression is used. Reports upload even if a scan fails.

Build-only pip/setuptools are removed after dependency installation, reducing the runtime image and eliminating vulnerable installer/vendor components.

Production credentials are not needed: publishing authenticates with the short-lived GitHub Actions `GITHUB_TOKEN` scoped to `packages: write`. The Kubernetes cluster is disposable on the runner. The image is loaded from that runner's Docker daemon, using exactly the published SHA tag, so the demo does not require a long-lived registry pull credential. A permanent cluster would need registry access and its own deployment identity.

The original dashboard endpoint `/api/pipeline/run` is a visual simulation. It does not execute deployments or security scans. Evidence of actual execution comes from GitHub Actions and the scanner reports.
