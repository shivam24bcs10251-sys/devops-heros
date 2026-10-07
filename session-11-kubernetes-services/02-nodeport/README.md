# NodePort hands-on lab

NodePort exposes Nginx on node port 30080 as well as the internal Service port 80. Two Deployment replicas are selected. On this Mac, a persistent Minikube service tunnel provides host access.

## Manifests

- [app-deployment.yaml](app-deployment.yaml)
- [service.yaml](service.yaml)

## Run and verify

Run from the Session 11 folder after creating `namespace.yaml`:

```bash
kubectl -n session11 apply -f 02-nodeport/
kubectl -n session11 get svc web-service-nodeport
```

See the [NodePort section in the complete submission](../README.md) for rollout, DNS, endpoint and connectivity commands, observations, environment setup and cleanup.

![Live NodePort verification](../Output/02-nodeport.png)

[Actual terminal transcript](../Output/logs/02-nodeport.txt).
