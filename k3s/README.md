# k3s

#### Install k3s & create k3s cluster in the VM

```bash
curl -sfL https://get.k3s.io |INSTALL_K3S_VERSION="v1.24.7+k3s1" sh -
kubectl get nodes
kubectl create ns practice
kubectl run nginx --image=nginx:latest
```
#### Inspect the nodes
```
kubectl get nodes 
k3s kubectl get nodes
```

#### Run a test pod
```
kubectl run nginx --image=nginx && kubectl get pods --watch
```

#### Destroy the cluster and uninstall k3s
```
k3s-killall.sh && k3s-uninstall.sh
```
