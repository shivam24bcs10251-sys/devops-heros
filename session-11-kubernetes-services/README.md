# Session 11: Kubernetes Services

This session covers the main Kubernetes Service types used to expose and discover applications inside and outside a cluster.

## Topics Covered

| No. | Topic | Description |
| --- | --- | --- |
| 01 | [ClusterIP](./01-clusterip) | Default internal service type for stable pod-to-pod communication inside the cluster. |
| 02 | [NodePort](./02-nodeport) | Exposes an application on a static port across worker nodes for external access. |
| 03 | [LoadBalancer](./03-loadbalancer) | Uses a cloud provider load balancer to expose applications publicly. |
| 04 | [ExternalName](./04-externalname) | Creates an internal DNS alias for an external service or domain. |
| 05 | [Headless Service](./05-headless) | Disables ClusterIP and returns individual pod DNS records for direct pod discovery. |

## Output Screenshots

### 01. ClusterIP

![ClusterIP output](./Output/01-clusterip.png)

### 02. NodePort

![NodePort output](./Output/02-nodeport.png)

### 03. LoadBalancer

![LoadBalancer output](./Output/03-loadbalancer.png)

### 04. ExternalName

![ExternalName output](./Output/04-externalname.png)

### 05. Headless Service

![Headless Service output](./Output/05-headless.png)

