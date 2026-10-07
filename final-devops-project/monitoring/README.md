# LabLedger monitoring

Install these scoped Kubernetes manifests after the application namespace exists:

```bash
kubectl apply -f monitoring/
kubectl rollout status deploy/session21-prometheus -n session21
kubectl rollout status deploy/session21-grafana -n session21
kubectl port-forward -n session21 svc/session21-prometheus 9091:9090
kubectl port-forward -n session21 svc/session21-grafana 3005:3000
```

Open http://127.0.0.1:9091/targets and http://127.0.0.1:3005/d/labledger. Prometheus discovers each backend Pod and scrapes its /metrics endpoint. Role/RoleBinding permit read-only Pod discovery within session21 only. Grafana provisions the datasource and six-panel dashboard, with anonymous Viewer access for this loopback classroom setup. Prometheus 3.15.0 and Grafana 12.1.1 match the verified Session 20 monitoring stack.

The dashboard shows request throughput, up targets, p95 HTTP latency, RSS memory, per-handler traffic and CPU as percent of one core. Application counters/histograms come from the real FastAPI instrumentator; Linux process metrics come from prometheus-client. Resource metrics and kubectl top depend separately on Metrics Server. Logs use JSON with request ID, method/path/status, duration and release SHA. No distributed trace export is claimed.

Alert rules evaluate unavailable scrape targets and a sustained 5xx ratio over 5%. Prometheus displays firing/resolved alert states; this lab has no external notification receiver. History is stored in emptyDir and is lost when monitoring Pods are replaced. A production installation needs persistent retention, authenticated dashboard access, TLS and an Alertmanager receiver.
