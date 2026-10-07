#!/usr/bin/env bash
# Synthetic CPU load inside the initial Nginx replicas, bounded to 180 seconds.
set -euo pipefail
pids=()
trap 'for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done' EXIT
for pod in $(kubectl --context="${KUBE_CONTEXT:-devops-assignment}" -n production-webapp get pods -l app=web-app -o jsonpath='{.items[*].metadata.name}'); do
  (kubectl --context="${KUBE_CONTEXT:-devops-assignment}" -n production-webapp exec "$pod" -- sh -c 'timeout 180 sh -c "while :; do :; done"' || { code=$?; test "$code" -eq 124 || test "$code" -eq 143; }) &
  pids+=("$!")
done
for pid in "${pids[@]}"; do wait "$pid"; done
