#!/usr/bin/env bash
set -euo pipefail
: "${IMAGE:?Set IMAGE to the built and published immutable image tag}"
kind create cluster --name session17 --wait 120s
trap 'kind delete cluster --name session17' EXIT
# Load exactly the image that passed the scan and was pushed, including its digest.
kind load docker-image "$IMAGE" --name session17
sed "s|__IMAGE__|$IMAGE|g" k8s/deployment.yaml | kubectl apply -f -
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/session17-python --timeout=120s
kubectl get pods,services
kubectl get pods -l app=session17-python -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.containerStatuses[0].imageID}{"\n"}{end}'
kubectl port-forward service/session17-python 5001:80 > /tmp/session17-forward.log 2>&1 &
for attempt in {1..30}; do
  if curl --fail --silent http://localhost:5001/health > /tmp/session17-health.json; then break; fi
  sleep 1
done
python -c 'import json; data=json.load(open("/tmp/session17-health.json")); assert data["status"] == "healthy"; print("Health verified:", data["status"])'
curl --fail --silent -H 'Content-Type: application/json' -d '{"number1":10,"number2":20}' http://localhost:5001/api/add > /tmp/session17-add.json
python -c 'import json; data=json.load(open("/tmp/session17-add.json")); assert data["result"] == 30; print("API verified:", data)'
curl --fail --silent http://localhost:5001/ | head -c 250
printf '\nDeployment verified successfully.\n'
