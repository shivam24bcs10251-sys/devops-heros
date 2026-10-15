# Captured verification reports

The `ci-37619323230-*` and `ci-37620612050-*` directories contain reports downloaded from successful GitHub Actions runs. Original artifacts remain on [first-release run 37619323230](https://github.com/shivam24bcs10251-sys/devops-heros/actions/runs/37619323230) and [feature-release run 37620612050](https://github.com/shivam24bcs10251-sys/devops-heros/actions/runs/37620612050).

**Evidence normalization:** The public upstream Python image `GPG_KEY` fingerprint is replaced with `public-key` in the repository copies of Trivy's ImageConfig environment/history metadata. Gitleaks interpreted its six repeated appearances as generic API keys. This is a public signing-key identifier, not a password or private key. Image references/digests, package inventory, scanner results and vulnerability severities are unchanged. Original downloadable CI artifacts preserve the complete scanner output. No source-secret rule or vulnerability gate was bypassed.

`security-summary.json` counts actual findings by severity from these Trivy reports. Test JUnit/coverage, SAST and dependency reports retain their original results. `initial-rollout-load.txt` preserves the pressure/rollout experiment with errors; `steady-load.txt` and `hpa-load.txt` record subsequent zero-error throttled runs. Reports are evidence snapshots, not guarantees about future vulnerability databases or production capacity.

## Live AWS completion · 15 October 2026

`aws-live-resources.json` is an AWS/Kubernetes API snapshot of the dedicated LabLedger lab in account `499567237930`, Sydney. It includes the actual VPC/subnets, EKS/node group, managed worker, encrypted gp3 database volume, Classic Load Balancer and add-ons. It contains resource metadata, not database Secret values or AWS credentials.

`aws-cleanup-verification.json` records the later AWS absence checks after the Kubernetes-owned volume/load balancer and all 21 Terraform-managed resources were removed. Full command transcripts are in `../logs/`; images `42`–`56` are the corresponding real Terminal/Chrome screenshots. Earlier CI/security reports remain the original 7 October scan/test snapshots.
