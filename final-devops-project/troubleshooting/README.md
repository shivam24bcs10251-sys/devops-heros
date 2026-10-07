# Troubleshooting lab · observed failures and recovery

All experiments target the `session21` lab namespace. Record the working backend image before experimenting. Never delete the database PVC. Pause automatic GitOps reconciliation so self-healing does not erase the symptom before it is investigated:

```bash
IMAGE=$(kubectl get deploy labledger-backend -n session21 -o jsonpath='{.spec.template.spec.containers[0].image}')
kubectl patch application labledger -n session20-argocd --type=merge \
  -p '{"spec":{"syncPolicy":{"automated":null}}}'
```

After every repair, check HTTP behavior and the relevant Kubernetes resource. Restore `kubectl apply -f gitops/application.yaml` after the entire lab and wait for Synced/Healthy. Screenshots and command transcripts are linked in the main README.

## 1. Invalid image tag blocks a rollout

**Identify:** A newly created backend Pod cannot pull its image. Existing replicas remain available, so a successful API request alone does not prove the new release deployed.

**Investigate:** Compare the Deployment image with Pod events and check available replicas. The event identifies the missing registry image/tag.

**Root cause:** The deliberately injected `missing-lab-tag` is not a published release.

```bash
kubectl set image deploy/labledger-backend -n session21 \
  backend=ghcr.io/shivam24bcs10251-sys/labledger-backend:missing-lab-tag
kubectl get pods -n session21 -l app=labledger-backend
kubectl get events -n session21 --field-selector reason=Failed --sort-by=.lastTimestamp
# Repair with the previously recorded verified image.
kubectl set image deploy/labledger-backend -n session21 backend="$IMAGE"
kubectl rollout status deploy/labledger-backend -n session21 --timeout=120s
curl -fsS http://labledger.localhost:8086/health
```

**Verify:** Rollout completes, ready backend replicas remain available and `/health` reports the verified release SHA. [Failure](../Output/19-fault-image.png) · [Recovery](../Output/20-fix-image.png).

## 2. Service selector mismatch returns HTTP 503

**Identify:** API traffic through Ingress fails with 503 while backend Pods are running.

**Investigate:** Read the Service selector, actual Pod labels and EndpointSlices. The wrong selector produces no backend endpoints.

**Root cause:** `app=labledger-wrong` cannot select Pods labeled `app=labledger-backend`.

```bash
kubectl patch svc backend -n session21 --type=merge \
  -p '{"spec":{"selector":{"app":"labledger-wrong"}}}'
kubectl get svc backend -n session21 -o jsonpath='{.spec.selector}'
kubectl get pods -n session21 -l app=labledger-backend --show-labels
kubectl get endpointslices -n session21 -l kubernetes.io/service-name=backend
curl -s -o /dev/null -w '%{http_code}\n' http://labledger.localhost:8086/api/assets
kubectl patch svc backend -n session21 --type=merge \
  -p '{"spec":{"selector":{"app":"labledger-backend"}}}'
```

**Verify:** Endpoints reappear and API traffic returns 200. [Failure](../Output/21-fault-service.png) · [Recovery](../Output/22-fix-service.png).

## 3. Ingress routes to a closed port and returns HTTP 502

**Identify:** An Ingress path routes traffic to a declared Service port whose target is not listening.

**Investigate:** Compare the Ingress port, Service port/targetPort, EndpointSlice ports and backend container port. The app listens on 8000; the injected endpoint uses 8080.

**Root cause:** The route is syntactically valid but points to a closed backend port. An earlier experiment referencing a nonexistent Service port was rejected by Traefik with `service port not found`, while the previous valid route stayed live. This is why controller logs matter even when a cached route returns 200.

```bash
kubectl patch svc backend -n session21 --type=merge \
  -p '{"spec":{"ports":[{"name":"http","port":8000,"targetPort":8000},{"name":"fault","port":8080,"targetPort":8080}]}}'
kubectl patch ingress labledger -n session21 --type=json \
  -p '[{"op":"replace","path":"/spec/rules/0/http/paths/0/backend/service/port/number","value":8080}]'
kubectl get svc backend -n session21
kubectl get endpointslices -n session21 -l kubernetes.io/service-name=backend
curl -s -o /dev/null -w '%{http_code}\n' http://labledger.localhost:8086/api/assets
# Restore the listening port and remove the fault-only Service port.
kubectl patch ingress labledger -n session21 --type=json \
  -p '[{"op":"replace","path":"/spec/rules/0/http/paths/0/backend/service/port/number","value":8000}]'
kubectl patch svc backend -n session21 --type=merge \
  -p '{"spec":{"ports":[{"name":"http","port":8000,"targetPort":8000}]}}'
```

**Verify:** After the controller observes the fix, API traffic returns 200. [Failure](../Output/23-fault-ingress.png) · [Recovery](../Output/24-fix-ingress.png).

## 4. Database outage separates liveness from readiness

**Identify:** Direct backend `/health` remains 200 while `/ready` becomes 503 after PostgreSQL is stopped.

**Investigate:** Inspect the StatefulSet/Pods, backend readiness response and persistent volume claim. A port-forward directly to the still-running backend is used so a Service's readiness filtering does not conceal the response.

**Root cause:** The DB has zero replicas. The process is alive, but a request requiring migrated tables cannot succeed.

```bash
curl -fsS http://127.0.0.1:8121/api/stats
kubectl scale statefulset labledger-postgres -n session21 --replicas=0
kubectl wait --for=delete pod/labledger-postgres-0 -n session21 --timeout=60s
curl -s -w '\n%{http_code}\n' http://127.0.0.1:8121/health
curl -s -w '\n%{http_code}\n' http://127.0.0.1:8121/ready
kubectl get pvc -n session21
kubectl scale statefulset labledger-postgres -n session21 --replicas=1
kubectl rollout status statefulset/labledger-postgres -n session21 --timeout=120s
kubectl wait --for=condition=Ready pod -l app=labledger-backend -n session21 --timeout=120s
curl -fsS http://127.0.0.1:8121/ready
curl -fsS http://127.0.0.1:8121/api/stats
```

**Verify:** Readiness returns 200. Before/after counts match exactly: **7 equipment types, 30 total units, 26 available, 4 on loan, 3 active loans**. The same PVC remains bound, proving persistence across DB Pod replacement. Later live verification adds more labeled fixtures. [Failure](../Output/25-fault-database.png) · [Recovery](../Output/26-fix-database.png).

## Additional observation: shared-node pressure during a rollout

The first 32-worker, unthrottled, 120-second inventory traffic run overlapped the GitOps rollout. HPA observed 314% CPU relative to requests and requested four replicas. During this run, Metrics Server's one-second probes timed out and restarted its container; metrics briefly became unavailable. The app accepted **11,710 requests with 299 errors** during that combined pressure/rollout test. This is an operational limitation, not a zero-error capacity claim.

Inspection used `kubectl describe pod -n kube-system -l k8s-app=metrics-server`, HPA events, Pod readiness and the recorded load counts. After traffic stopped, Metrics Server recovered, HPA reduced to two replicas and Argo CD returned Healthy. A subsequent throttled workload tests steady operation separately. The [bounded read-only tool](load.py) supports an interval, maximum 300 seconds and at most 64 workers; use the default modest workload for routine demonstrations.

The initial results are retained in [the load report](../Output/reports/initial-rollout-load.txt), and the main README includes the pressure and recovery screenshots. Raising available cluster CPU, staggering deployments/load tests and tuning monitoring probes are future capacity improvements; no unrelated cluster configuration was changed to hide the result.
