# Terraform: real AWS VPC and EKS

**Live AWS deployment is pending permissions.** The configured IAM identity cannot even describe EC2 VPCs. Validation/mock tests do not constitute a live AWS plan, EKS deployment or destroy. See the final project README for actual execution evidence.

This classroom architecture provisions a VPC, two public subnets, IGW/routes, EKS 1.35 and one managed AL2023 worker node (maximum two), plus EBS CSI and Metrics Server add-ons. Public worker networking avoids a NAT gateway for this short lab; EKS API access is limited to the current workstation /32 and private access stays enabled. There are no SSH keys or SSH ingress rules. Production should use private nodes, workload identities, TLS and an external/managed PostgreSQL database.

## Run when AWS access is available

```bash
cp terraform.tfvars.example terraform.tfvars
# Set the authorized AWS profile and your current public IPv4/32.
terraform init
terraform fmt -check
terraform validate
terraform plan -out=lab.tfplan
terraform apply lab.tfplan
terraform output
# Run the emitted update-kubeconfig command.
kubectl get nodes
```

The administrator must authorize EC2/VPC, EKS, required IAM role/policy operations and iam:PassRole, plus CloudFormation/service-linked-role actions if required by the account. Credentials come from a local AWS profile; never write access keys to Terraform variables or Git.

EBS CSI uses a dedicated IAM role through EKS Pod Identity; the agent and association are declared in Terraform. After deployment, create a `gp3` StorageClass using `ebs.csi.aws.com`, encrypted volumes and WaitForFirstConsumer; pass it in Helm's `postgres.storageClass`. Install Traefik with a LoadBalancer Service, set the actual DNS/host, and install Prometheus/Grafana from monitoring/. Set aside time for provisioning, verification and destruction. AWS resources incur charges while they exist; this repository does not claim a cost cap or free-tier eligibility.

## Tear down and verify

Remove the application's PVC after evaluation and allow the CSI driver to remove its EBS volume before deleting EKS. Remove ingress LoadBalancer resources before the network is destroyed.

```bash
kubectl delete application labledger -n session20-argocd --ignore-not-found
kubectl delete namespace session21
# Wait for lab EBS volumes and load balancer resources to be removed.
terraform plan -destroy -out=destroy.tfplan
terraform apply destroy.tfplan
terraform state list
```

Confirm no lab EKS/node groups, EC2 instances, EBS volumes or load balancers remain. State, plans and real tfvars are ignored. Screenshots of actual cloud resources and successful destruction must be added only after this succeeds.

References: [EKS versions](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html), [EKS public subnet requirements](https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html), [EBS CSI](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html).
