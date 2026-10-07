# Session 20 mini-project

The supplied two-replica mini-project now serves JSON health responses, real Linux process CPU/RSS metrics and correlated JSON logs. Argo CD watches this repository's Session 20 branch and the `app/` directory. Its Application and restricted AppProject are in `gitops/`, outside the watched workload directory. Monitoring is bootstrapped separately from `monitoring/`.

## Reproduce

Use the existing local Minikube profile `devops-assignment`, or create an equivalent local cluster and replace the context below. Push application manifests before creating the Argo CD Application.

```bash
kubectl config use-context devops-assignment
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update argo
helm upgrade --install session20-argocd argo/argo-cd --version 10.9.7 \
  --namespace session20-argocd --create-namespace -f gitops/values.yaml --wait --timeout 10m
kubectl apply -f gitops/project.yaml
kubectl apply -f gitops/argocd-application.yaml
kubectl wait --for=jsonpath='{.status.sync.status}'=Synced application/session20-mini -n session20-argocd --timeout=300s
kubectl rollout status deployment/session20-mini -n session20 --timeout=300s
kubectl apply -f monitoring/
kubectl rollout status deployment/session20-prometheus -n session20 --timeout=300s
kubectl rollout status deployment/session20-grafana -n session20 --timeout=300s
```

Run each port-forward in its own terminal (bound to loopback):

```bash
kubectl port-forward -n session20 svc/session20-mini 8084:80
kubectl port-forward -n session20 svc/session20-prometheus 9090:9090
kubectl port-forward -n session20 svc/session20-grafana 3000:3000
```

Open Grafana at http://127.0.0.1:3000/d/session20 and Prometheus at http://127.0.0.1:9090. Grafana's classroom dashboard is anonymously readable and has no initial admin account; services remain ClusterIP. Monitoring history uses emptyDir and is lost on Pod replacement.

## Demonstrations

```bash
curl -fsS http://127.0.0.1:8084/health
curl -fsS -H 'X-Trace-ID: session20-request-001' http://127.0.0.1:8084/work
kubectl top pods -n session20
kubectl logs -l app=session20-mini -n session20 --tail=5 --prefix=true
python3 tools/query.py 'sum(process_resident_memory_bytes{job="session20-app"})'
```

The port-forward connects to one selected Pod, so the following failure applies to that Pod only. TCP probes deliberately keep the Pod available during a simulated dependency failure, allowing `/metrics` to remain scraped. This distinguishes HTTP application health from Pod Ready. Demo controls use GET for convenience in this isolated exercise; omit them in production.

```bash
curl -fsS http://127.0.0.1:8084/demo/fail
curl -s -o /dev/null -w 'HTTP health status: %{http_code}\n' http://127.0.0.1:8084/health
# After the next scrape and 10 seconds in the failed state:
python3 tools/alerts.py
curl -fsS http://127.0.0.1:8084/demo/recover
# After the next rule evaluation:
python3 tools/alerts.py
```

Prometheus evaluates and displays real firing alerts. An external Alertmanager notification receiver is outside this demo; no email or paging notification is claimed.

## GitOps exercise

1. Start with two replicas and `APP_VERSION=v1` in Git. Wait for Synced/Healthy.
2. Change Git's replicas to three and version to v2; commit and push this branch. Argo CD detects the Git change and rolls out Kubernetes automatically.
3. Manually scale the Deployment to one. Observe drift, then Argo CD's self-heal returning it to Git's three.
4. Revert Git's replicas to two, commit/push, and observe reconciliation. Final desired state has two replicas and v2.

No `kubectl apply -f app/` or direct apply of changed Deployment manifests is used for Git-managed releases. Root README screenshots/logs record the actual Git revisions and observed states.

## Cleanup

```bash
kubectl delete application session20-mini -n session20-argocd
kubectl delete namespace session20
helm uninstall session20-argocd -n session20-argocd
kubectl delete namespace session20-argocd
```

This affects the two lab namespaces only; do not delete the shared cluster. Argo CD CRDs installed by Helm may remain for reuse.
