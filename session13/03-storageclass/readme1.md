# Dynamic provisioning

dynamic-pvc requests 500Mi from StorageClass standard in namespace session13. Minikube supplies a PV through its hostpath provisioner. See [volume documentation](../01-kubernetes-volumes/README.md) and [actual binding evidence](../README.md).
