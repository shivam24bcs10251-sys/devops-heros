#!/usr/bin/env bash
set -euo pipefail
kubectl --context="${KUBE_CONTEXT:-devops-assignment}" delete namespace session12
