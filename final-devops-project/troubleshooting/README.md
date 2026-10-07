# Controlled troubleshooting lab

Run these only against the lab namespace. The final README records observed symptoms, investigation, root cause, fix and verification for each fault. Preserve the database PVC. Pause Argo CD automatic sync during manual fault investigation, then restore its automated policy and verify Git desired state.

1. Invalid backend image tag → image pull failure. Inspect Pod/events/image, restore the Git-declared image.
2. Wrong backend Service selector → empty EndpointSlices and failed API traffic. Compare selector/Pod labels, restore the correct selector.
3. Wrong Ingress backend port → HTTP 502. Compare declared Ingress port with Service port 8000, restore the correct route.
4. Stop PostgreSQL → backend readiness fails, while cheap /health still returns UP. Inspect /ready, backend logs, StatefulSet/Pod; restore one database replica and verify records survive in the PVC.
