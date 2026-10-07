# Session 13 mini-project

The completed [Session 13 submission](../README.md) contains actual persistence, Service, probes and HPA evidence for these supplied manifests.

Apply namespace.yaml before the other YAML files. The two initial Nginx replicas share web-data on the single Minikube node. The student file is read from a replacement Pod after deleting the writer. startupProbe, readinessProbe and livenessProbe request / on port 80. The HPA measures CPU against a 100m request, targets 50%, and permits 2–5 replicas.

The bounded load-generator.sh runs synthetic CPU load in the two initial replicas for 180 seconds. Inspect HPA and kubectl top pods while it runs. It is a CPU demonstration; it does not pretend to be HTTP traffic. The main 04-hpa lab separately uses an HTTP load-generator Pod. Scale-down uses a 30-second demonstration stabilization window.
