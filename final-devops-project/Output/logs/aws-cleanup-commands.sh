#!/usr/bin/env bash
set -euo pipefail
export AWS_PROFILE=scaler-sst AWS_REGION=ap-southeast-2 AWS_PAGER=""
export KUBECONFIG="$PWD/.local/kubeconfig"
test "$(aws sts get-caller-identity --query Account --output text)" = "499567237930"
test "$(terraform -chdir=terraform output -raw cluster_name)" = "labledger-session21"
test "$(kubectl config current-context)" = "arn:aws:eks:ap-southeast-2:499567237930:cluster/labledger-session21"
date -u
kubectl get pvc -n session21
kubectl delete namespace session21 --ignore-not-found --wait=true --timeout=5m
if kubectl get pv pvc-4a38ed98-c05d-47d9-994b-20314425fa43 >/dev/null 2>&1; then
  kubectl wait --for=delete pv/pvc-4a38ed98-c05d-47d9-994b-20314425fa43 --timeout=5m
fi
aws ec2 wait volume-deleted --volume-ids vol-0161ab3c9dd4831d9
printf 'Database namespace, PV and encrypted EBS volume removed.\n'
kubectl delete namespace labledger-ingress --ignore-not-found --wait=true --timeout=5m
for attempt in {1..60}; do
  LB_COUNT="$(aws elb describe-load-balancers --query "length(LoadBalancerDescriptions[?LoadBalancerName=='a8ea0bdf04a1744448c3028e6dfef7f0'])" --output text)"
  [[ "$LB_COUNT" == 0 ]] && break
  sleep 5
done
test "$LB_COUNT" = 0
printf 'Dedicated ingress namespace and Classic Load Balancer removed.\n'
terraform -chdir=terraform plan -destroy -input=false -no-color -out=destroy.tfplan
terraform -chdir=terraform apply -input=false -no-color destroy.tfplan
terraform -chdir=terraform state list
date -u
