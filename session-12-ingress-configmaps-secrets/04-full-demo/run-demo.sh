#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
kube() { kubectl --context="${KUBE_CONTEXT:-devops-assignment}" "$@"; }
kube apply -f namespace.yaml
kube -n session12 create secret generic yatri-db-secret --from-literal=POSTGRES_USER=demo-user --from-literal=POSTGRES_PASSWORD=demo-session12-only --from-literal=POSTGRES_DB=demo-db --dry-run=client -o yaml | kube apply -f -
for manifest in configmap frontend backend ingress; do
  kube apply -f "04-full-demo/$manifest.yaml"
done
kube -n session12 rollout status deployment/yatri-frontend --timeout=180s
kube -n session12 rollout status deployment/yatri-backend --timeout=180s
kube -n session12 get configmap,secret,service,ingress
