# Kubernetes volumes

| Object | Lifetime and purpose | Practical example in this session |
| --- | --- | --- |
| emptyDir | Created for a Pod; shared by its containers; survives container restarts but is removed with that Pod. | Writer and reader containers access the same /data/message.txt. |
| hostPath | Mounts a directory on the Kubernetes node; survives replacement on that node but is node-local. | /tmp/session13-hostpath-data is mounted at /data. On Minikube's Docker driver this is inside the node container, not a Mac host folder. |
| PersistentVolume | Cluster-scoped representation of storage, with capacity, access modes and reclaim policy. | session13-static-pv uses an explicitly created node directory and Retain policy. |
| PersistentVolumeClaim | Namespaced request for storage; a bound claim can be mounted by Pods. | student-pvc binds to the named static PV; mini-project web-data outlives Pod replacement. |
| StorageClass | Defines a provisioner and parameters for dynamically supplying PVs. | standard uses the Minikube hostpath provisioner. |
| Dynamic provisioning | The provisioner creates backing storage and a PV when a PVC requests a supported class. | dynamic-pvc and mini-project web-data bind without writing a PV manifest for each claim. |

The static claim uses storageClassName: "" and volumeName: session13-static-pv so it binds to the supplied PV rather than requesting the default dynamic provisioner. The dynamic claim explicitly requests standard. The mini-project uses the cluster's default StorageClass.

ReadWriteOnce permits a volume to be mounted read-write by one node. Multiple Pods on that same node can mount it; it does not mean exactly one Pod. This lab uses a single node. A production multi-node app would need an appropriate storage driver and sharing/access-mode design.

The static PV retains its storage when its claim is removed. A dynamically provisioned PV uses the StorageClass reclaim policy; inspect it rather than assuming data will be retained. emptyDir and node-local hostPath are different from storage that can follow workloads between nodes.

See the [complete submission](../README.md) for commands, actual PVC/PV output, shared-volume verification and before/after persistence evidence.

Sources: [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/), [Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), [Storage classes](https://kubernetes.io/docs/concepts/storage/storage-classes/).
