#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
lab_context="${KUBE_CONTEXT:-devops-assignment}"
kube() { kubectl --context="$lab_context" "$@"; }
kube apply -f namespace.yaml
for folder in 01-clusterip 02-nodeport 03-loadbalancer 04-externalname 05-headless; do
  kube -n session11 apply -f "$folder/"
done
for deployment in web-app-clusterip web-app-nodeport web-app-loadbalancer; do
  kube -n session11 rollout status "deployment/$deployment" --timeout=180s
done
kube -n session11 rollout status statefulset/web-stateful --timeout=180s
kube -n session11 wait --for=condition=Ready pod/curl-client pod/dns-test-client pod/headless-dns-client --timeout=180s
kube -n session11 get services
kube -n session11 get pods
kube -n session11 exec curl-client -- wget -qO- http://web-service-clusterip:8080
kube -n session11 exec dns-test-client -- nslookup -type=CNAME external-database-service.session11.svc.cluster.local
kube -n session11 exec dns-test-client -- wget -S -O /dev/null --header 'Host: example.com' http://external-database-service
kube -n session11 exec headless-dns-client -- wget -qO- http://web-stateful-0.web-service-headless.session11.svc.cluster.local
printf '\nFor host NodePort and LoadBalancer tests, start the tunnels described in README.md.\n'
