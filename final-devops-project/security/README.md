# Security gates

The pipeline blocks on failed API tests/coverage, Bandit SAST findings, Python dependency audit findings, high/critical npm dependency findings, Gitleaks secret detections, or high/critical Trivy image vulnerabilities in either runtime image. Security runs before SHA-tagged images are published. There are no CVE ignore files or `continue-on-error` gates. Runtime dependencies are pinned with their transitive dependencies; frontend uses npm ci and a committed lock file.

Backend and frontend run as UID 10001 and 101 respectively. Kubernetes drops all capabilities, denies privilege escalation and uses RuntimeDefault seccomp. Application Pods do not mount service-account tokens. Credentials are externally bootstrapped into a Kubernetes Secret and local Compose reads an ignored .env generated with a random password. Generated Secrets are sent to kubectl through stdin and never printed or committed. Prometheus has namespace-scoped Pod discovery only.

Image builds update the base OS packages; the Python runtime removes build/install tooling after dependencies are installed, reducing unnecessary pip/setuptools attack surface. Trivy examines both the OS and installed language packages. A clean report means no findings at the gate's severities in that database snapshot; it does not imply the app has no security flaws. Scanner versions and reports are recorded in the final README/evidence.

This classroom UI uses synthetic borrower names and a local HTTP route. It has no user authentication/authorization and is not suitable for public production access as-is. Production requires authentication, TLS, controlled network ingress, backup/restore, image digests/signatures, managed secrets, appropriate database access and persistent telemetry retention.
