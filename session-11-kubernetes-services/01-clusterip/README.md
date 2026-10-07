# ClusterIP hands-on lab

ClusterIP supplies a virtual IP for communication inside the cluster. This manifest forwards Service port 8080 to Nginx port 80 on three matching Pods.

## Manifests

- [app-deployment.yaml](app-deployment.yaml)
- [client-pod.yaml](client-pod.yaml)
- [service.yaml](service.yaml)

## Run and verify

Run from the Session 11 folder after creating `namespace.yaml`:

```bash
kubectl -n session11 apply -f 01-clusterip/
kubectl -n session11 get svc web-service-clusterip
```

See the [ClusterIP section in the complete submission](../README.md) for rollout, DNS, endpoint and connectivity commands, observations, environment setup and cleanup.

![Live ClusterIP verification](../Output/01-clusterip.png)

[Actual terminal transcript](../Output/logs/01-clusterip.txt).
