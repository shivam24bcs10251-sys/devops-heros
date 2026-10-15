#!/usr/bin/env bash
# Deploy the verified LabLedger release to this project's Terraform-managed EKS.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"
export AWS_PROFILE="${AWS_PROFILE:-scaler-sst}"
export AWS_REGION="${AWS_REGION:-ap-southeast-2}" AWS_PAGER=""
EXPECTED_ACCOUNT_ID="${EXPECTED_ACCOUNT_ID:-499567237930}"
ACTUAL_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
if [[ "$ACTUAL_ACCOUNT_ID" != "$EXPECTED_ACCOUNT_ID" ]]; then
  printf 'Refusing deployment: expected AWS account %s, received %s.\n' "$EXPECTED_ACCOUNT_ID" "$ACTUAL_ACCOUNT_ID" >&2
  exit 1
fi
CLUSTER_NAME="$(terraform -chdir=terraform output -raw cluster_name)"
mkdir -p .local
chmod 700 .local
export KUBECONFIG="$PROJECT_DIR/.local/kubeconfig"
export HELM_REPOSITORY_CONFIG="$PROJECT_DIR/.local/helm/repositories.yaml"
export HELM_REPOSITORY_CACHE="$PROJECT_DIR/.local/helm/repository"
mkdir -p "$HELM_REPOSITORY_CACHE"
aws eks update-kubeconfig --name "$CLUSTER_NAME" --region "$AWS_REGION" --profile "$AWS_PROFILE" --kubeconfig "$KUBECONFIG"
chmod 600 "$KUBECONFIG"
kubectl get nodes
TRAEFIK_VERSION=41.6.1
if [[ ! -f ".local/traefik-$TRAEFIK_VERSION.tgz" ]]; then
  helm pull traefik --repo https://traefik.github.io/charts --version "$TRAEFIK_VERSION" --destination .local
fi
helm upgrade --install labledger-ingress ".local/traefik-$TRAEFIK_VERSION.tgz" \
  -n labledger-ingress --create-namespace \
  --set ingressClass.name=traefik --set resources.requests.cpu=50m --set resources.requests.memory=64Mi \
  --set resources.limits.memory=192Mi --wait --timeout 8m
INGRESS_HOST=""
for attempt in {1..60}; do
  INGRESS_HOST="$(kubectl get svc labledger-ingress-traefik -n labledger-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')"
  [[ -n "$INGRESS_HOST" ]] && break
  sleep 5
done
if [[ -z "$INGRESS_HOST" ]]; then printf 'LoadBalancer hostname was not assigned.\n' >&2; exit 1; fi
python3 scripts/bootstrap.py
kubectl apply -f kubernetes/storageclass-eks.yaml
helm lint helm/labledger -f gitops/values.yaml
helm upgrade --install labledger helm/labledger -n session21 \
  -f gitops/values.yaml --set postgres.storageClass=labledger-gp3 \
  --set-string ingress.host="$INGRESS_HOST" --wait --wait-for-jobs --timeout 10m
kubectl apply -f monitoring/
kubectl rollout status deployment/session21-prometheus -n session21 --timeout=300s
kubectl rollout status deployment/session21-grafana -n session21 --timeout=300s
APP_URL="http://$INGRESS_HOST"
APP_READY=false
for attempt in {1..60}; do
  if curl --fail --silent --connect-timeout 5 "$APP_URL/ready" >/dev/null; then APP_READY=true; break; fi
  sleep 5
done
if [[ "$APP_READY" != true ]]; then printf 'Ingress readiness did not succeed.\n' >&2; exit 1; fi
python3 scripts/seed.py "$APP_URL"
RELEASE_SHA="$(helm get values labledger -n session21 -o json | python3 -c 'import json,sys; print(json.load(sys.stdin)["backend"]["tag"])')"
python3 scripts/verify.py --base "$APP_URL" --version "$RELEASE_SHA"
printf '%s\n' "$APP_URL" > .local/aws-url.txt
kubectl get deploy,statefulset,pods,svc,ingress,pvc,hpa -n session21
printf '\nLabLedger AWS deployment verified: %s\n' "$APP_URL"
printf 'Monitoring remains private; use loopback kubectl port-forward commands from the README.\n'
