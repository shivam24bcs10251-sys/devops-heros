# LabLedger evidence index

All PNGs are real native Terminal or Chrome window screenshots. Capture helpers run separately; no generated mockups or invented cloud/monitoring results are used. Text files in `logs/` retain the command output. The project README embeds every screenshot with a caption and transcript link.

| Range | Date | Evidence |
|---|---|---|
| 01–10 | 7 October 2026 | Source/branch, tests, security, Docker, Terraform validation, historical AWS denial and browser views |
| 11–18 | 7 October 2026 | Local Helm/Kubernetes, storage/config, metrics, PostgreSQL and GitOps |
| 19–27 | 7 October 2026 | Four faults, investigation, repair and request-log correlation |
| 28–41 | 7 October 2026 | CI/security, GHCR, autoscaling, final GitOps release, commit history and tests |
| 42–46 | 15 October 2026 | Scaler AWS identity, live 21-resource plan/apply, VPC/EKS Console |
| 47–51 | 15 October 2026 | Healthy cloud add-ons/workloads, AWS application, live business checks, encrypted storage and metrics |
| 52–54 | 15 October 2026 | Cloud Prometheus/Grafana and unchanged infrastructure |
| 55–56 | 15 October 2026 | Actual teardown and AWS absence checks |

## Reading the cloud record

- `reports/aws-live-resources.json`: AWS/Kubernetes metadata while the LabLedger lab existed. The EC2 request `ClientToken` field is omitted from the public report.
- `logs/aws-plan.txt` and `logs/aws-apply.txt`: full original 21-resource creation records.
- `logs/aws-labledger-deploy.txt`: completed reproducible deployment and PostgreSQL verification.
- `logs/aws-read-only-traffic.txt`: bounded inventory traffic used to populate monitoring; 644 successful requests and zero errors.
- `logs/aws-cleanup-commands.sh`: exact account/context-guarded teardown commands executed for this run.
- `logs/aws-destroy-full.txt`: Kubernetes-owned EBS/load-balancer removal, Terraform destroy and final state.
- `reports/aws-cleanup-verification.json`: AWS checks of the recorded resources after teardown.

Images `08` and its transcript document the earlier different-account access failure. They do not describe the successful Scaler-account run. Earlier CI/security reports are dated snapshots, not newly executed scans. The cleanup report refers only to the fresh LabLedger VPC/cluster and associated resources; the earlier TaskBoard deployment and unrelated accounts were preserved.
