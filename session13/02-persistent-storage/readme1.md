# Static PV and PVC

The PV is session13-static-pv with a node-local hostPath, DirectoryOrCreate, 1Gi capacity and Retain policy. student-pvc explicitly selects it using volumeName and an empty storageClassName. storage-demo mounts the bound claim at /data. See [the completed submission](../README.md) for live binding evidence and cleanup.
