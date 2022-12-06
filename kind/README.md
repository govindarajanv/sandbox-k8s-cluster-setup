# kind

```

#### Install kind in the VM
```
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

#### create a k8s cluster
```
kind create cluster --name=k8s --image=kindest/node:v1.24.0
```

#### Get Cluster info and kubeconfig
```
kubectl cluster-info --context kind-k8s
kind get clusters
kind get nodes --name k8s
kind get kubeconfig --name k8s

```

#### Inspect the nodes
```
kubectl get nodes
```

#### Run a test pod
```
kubectl run nginx --image=nginx && kubectl get pods --watch
```

#### Destroy the cluster
```
kind delete  cluster --name k8s
```
