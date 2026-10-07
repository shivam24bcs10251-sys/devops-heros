#!/usr/bin/env bash
set -euo pipefail
kind create cluster --name session16 --wait 120s
trap 'kind delete cluster --name session16' EXIT
kind load docker-image session16-calculator:demo --name session16
kubectl apply -f kubernetes.yaml
kubectl rollout status deployment/calculator --timeout=120s
kubectl get pods,services
kubectl port-forward service/calculator 8080:80 > /tmp/session16-forward.log 2>&1 &
for attempt in {1..30}; do
  if curl --fail --silent http://localhost:8080/health > /tmp/session16-health.json; then break; fi
  sleep 1
done
cat /tmp/session16-health.json
curl --fail --silent 'http://localhost:8080/calculate?op=add&a=10&b=5' > /tmp/session16-result.json
python -c 'import json; result=json.load(open("/tmp/session16-result.json")); assert result["result"] == 15; print("Deployment verified:", result)'
