# LabLedger · Session 21 DevOps Capstone

**Shivam Jaiswal · Campus equipment inventory and lending**

LabLedger is an original React, FastAPI and PostgreSQL application with stock-safe borrowing and returns. Its delivery path includes isolated tests, nonroot Docker images, GitHub Actions quality/security gates, SHA-tagged multiarchitecture GHCR releases, Kubernetes/Helm, Ingress, HPA, Prometheus/Grafana, GitOps and fault recovery.

**[Open the complete final project README](final-devops-project/README.md)** for architecture, reproducible setup, all 56 real screenshots, command transcripts and operating notes. [Session 21 submission map](session21-python/README.md) · [Evidence index](final-devops-project/Output/README.md).

The missing AWS work was completed on **15 October 2026** in **New Frontiers, account `499567237930`, Sydney (`ap-southeast-2`)**. A dedicated VPC, two public subnets, EKS cluster and managed worker were provisioned by Terraform. LabLedger, encrypted gp3 storage and private monitoring were verified, then the temporary lab was destroyed. Existing containers and unrelated AWS resources were preserved. Earlier local/CI evidence is dated 7 October; the new cloud evidence is dated 15 October.

![LabLedger running on AWS before teardown](final-devops-project/Output/49-aws-application-browser.png)

[Live AWS resource snapshot](final-devops-project/Output/reports/aws-live-resources.json) · [Verified cleanup](final-devops-project/Output/reports/aws-cleanup-verification.json) · [Terraform guide](final-devops-project/terraform/README.md).

## Course links

[Homework assignment](https://docs.google.com/document/d/1cjXFYf2Thm8cBEN-0C48B-v02cj3jGLd47lcO18prHE/edit?usp=sharing) · [Grading rubric](session21-python/GRADING.md).

Submission forms: [Section A](https://forms.gle/ydjAJcwxjpjBXgxB8) · [Section B](https://forms.gle/pAuXQaokwVzhRzit6).
