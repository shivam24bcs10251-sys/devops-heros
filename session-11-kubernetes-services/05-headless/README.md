# Headless Service hands-on lab

clusterIP: None makes DNS return individual ready Pod addresses. The governing Service and StatefulSet provide names web-stateful-0 through web-stateful-2. The direct request to ordinal 0 succeeds. No PVC is used in this networking example.

## Manifests

- [app-statefulset.yaml](app-statefulset.yaml)
- [client-pod.yaml](client-pod.yaml)
- [service.yaml](service.yaml)

## Run and verify

Run from the Session 11 folder after creating `namespace.yaml`:

```bash
kubectl -n session11 apply -f 05-headless/
kubectl -n session11 get svc web-service-headless
```

See the [Headless Service section in the complete submission](../README.md) for rollout, DNS, endpoint and connectivity commands, observations, environment setup and cleanup.

![Live Headless Service verification](../Output/05-headless.png)

[Actual terminal transcript](../Output/logs/05-headless.txt).
