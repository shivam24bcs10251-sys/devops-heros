# HPA exercise

See [the completed submission](../README.md) for actual idle, loaded and recovery evidence. This folder uses a bounded CPU-intensive Python HTTP handler, hpa-demo-service, the supplied 50% CPU HPA, and an eight-worker load-generator Pod. CPU request is 100m, limit 200m, and replicas range from 1 to 5. The 30-second scale-down stabilization is a demo setting.
