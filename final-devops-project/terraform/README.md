# Terraform · LabLedger AWS infrastructure

The live lab was executed on **15 October 2026**, in **account `499567237930`, Sydney (`ap-southeast-2`)**, using profile **`scaler-sst`**. The initial live plan created **21 managed resources**, including the VPC, two public subnets, EKS 1.35 and a managed worker. [The final project README](../README.md#aws-execution--15-october-2026) contains actual AWS Console, application, monitoring and teardown evidence.

## What Terraform manages

| Layer | Configuration |
|---|---|
| Network | Dedicated `10.21.0.0/16` VPC; two public `/24` subnets in separate AZs; internet gateway, route table and associations |
| Control plane | `labledger-session21`, Kubernetes 1.35; private endpoint enabled; public API restricted to supplied workstation IPv4 `/32` |
| Worker | One AL2023 x86_64 `c7i-flex.large` managed node; minimum 1, maximum 2; 20 GiB root disk; no SSH key |
| IAM | Separate cluster, worker and EBS roles with service trust and managed policy attachments |
| Storage identity | EKS Pod Identity agent and EBS CSI association; `AmazonEBSCSIDriverPolicyV2`; no IAM OIDC-provider creation |
| Add-ons | EBS CSI, Pod Identity agent and Metrics Server |
| Account protection | AWS provider `allowed_account_ids = [var.expected_account_id]` |

There is no NAT gateway. Public worker networking is a bounded classroom tradeoff; production should use private workers and an appropriate egress design. Terraform manages infrastructure; Helm/Kubernetes subsequently create the application, Classic Load Balancer and encrypted gp3 data volume. Those Kubernetes-owned resources must be removed before the cluster is destroyed.

The instance eligibility API was queried in this account/region before deployment; `c7i-flex.large` was eligible, while the earlier `t3.medium` choice was unsuitable for this account's free-plan restrictions. Eligibility does not make EKS, public IPv4, EBS or the load balancer cost-free.

## Provision

Run from `final-devops-project/terraform`:

```bash
export AWS_PROFILE=scaler-sst AWS_REGION=ap-southeast-2 AWS_PAGER=""
# Renew the existing CLI login if needed:
aws login --profile scaler-sst-login --region ap-southeast-2
aws sts get-caller-identity --query Account --output text
aws ec2 describe-instance-types --filters Name=free-tier-eligible,Values=true \
  --query 'InstanceTypes[].InstanceType' --output text
cp terraform.tfvars.example terraform.tfvars
# Edit admin_cidr to your current public IPv4/32.
# Keep the intended region/profile/account; use an available cluster name.
terraform init
terraform fmt -check -recursive
terraform validate
terraform test
terraform plan -out=create.tfplan
terraform apply create.tfplan
terraform output
```

The two Terraform tests use a mock AWS provider: they check two subnets, a restricted API, one initial worker and rejection of `0.0.0.0/0`. The separately recorded live plan/apply/API/Console checks establish that resources really existed. Keep the state after any partial apply; fix the cause and regenerate the plan instead of creating duplicate infrastructure.

Credentials are resolved by the AWS CLI profile, outside Git. Never place keys in HCL or tfvars. Real tfvars, `.terraform`, state, saved plans and `.local` kubeconfig/cache are ignored. The provider lock file is committed.

## Deploy the application

After Terraform apply completes, from `final-devops-project/`:

```bash
bash scripts/deploy-aws.sh
export KUBECONFIG="$PWD/.local/kubeconfig"
export AWS_PROFILE=scaler-sst AWS_REGION=ap-southeast-2
kubectl get nodes
kubectl get pods,svc,ingress,pvc,hpa -n session21
helm list -n session21
cat .local/aws-url.txt
```

The script checks the AWS account, writes a dedicated kubeconfig, uses an isolated Helm repository cache, installs pinned Traefik with the explicit `traefik` IngressClass, creates an external random database Secret through stdin, applies the encrypted `labledger-gp3` StorageClass and deploys the verified GHCR SHA from `gitops/values.yaml`. The actual ELB hostname becomes the Ingress host, so no external DNS registration is required. It then installs the private monitoring manifests, seeds synthetic equipment and runs real PostgreSQL/concurrency checks through the load balancer.

It does not start Docker, select the default kubeconfig or use another session's ingress controller. The EKS gp3 StorageClass is cloud-only. A single worker and ReadWriteOnce database volume do not provide database high availability.

## Monitoring access

```bash
export KUBECONFIG="$PWD/.local/kubeconfig"
kubectl port-forward -n session21 svc/session21-prometheus 19091:9090
# In another terminal with the same KUBECONFIG:
kubectl port-forward -n session21 svc/session21-grafana 13005:3000
```

Prometheus: `http://127.0.0.1:19091/targets`. Grafana: `http://127.0.0.1:13005/d/labledger`. Services stay ClusterIP; the anonymous Viewer dashboard is accessible through loopback forwards. Monitoring history uses ephemeral storage in this lab.

## Teardown in dependency order

This deletes the new lab's synthetic database. Use this project's dedicated kubeconfig and state. Do not run these commands against a shared or unrelated cluster.

```bash
# From final-devops-project/:
export AWS_PROFILE=scaler-sst AWS_REGION=ap-southeast-2
export KUBECONFIG="$PWD/.local/kubeconfig"
kubectl config current-context
kubectl get pvc -n session21
# Record the EBS volume ID before deleting the namespace.
kubectl get pv -o wide
kubectl delete namespace session21
# Wait for its PV/EBS volume to be removed while CSI and the worker still run.
kubectl get pv
kubectl delete namespace labledger-ingress
# Wait for the Classic Load Balancer and its ENIs/security group to disappear.
# For this disposable single-worker cluster only, after app/storage/LB removal:
# Remove the default CoreDNS PDB so the final worker can drain.
kubectl delete pdb coredns -n kube-system --ignore-not-found
terraform -chdir=terraform plan -destroy -out=destroy.tfplan
terraform -chdir=terraform apply destroy.tfplan
terraform -chdir=terraform state list
```

Verify the recorded cluster/node group, worker instance, data/root volumes, load balancer and VPC using AWS APIs. An empty Terraform state alone cannot prove that Kubernetes-created cloud resources were removed. Do not delete the shared local Minikube cluster, earlier AWS TaskBoard cluster or resources outside this lab's VPC. Cloud resource identifiers and the actual teardown outcome are recorded in the project evidence.

References: [EKS networking](https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html), [EBS CSI](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html), [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html).

During the recorded teardown, the last CoreDNS Pod was blocked by a zero-disruption PDB while its replacement was Pending on the cordoned single worker. After app data and the load balancer were removed, deleting that PDB in this disposable cluster allowed the worker to drain. [Observed state and exact fix](../Output/logs/aws-coredns-drain.txt).
