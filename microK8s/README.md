# Microk8s


#### Install microk8s in the VM
```
sudo snap install microk8s --classic
```

#### copy the cluster configuration
```
sudo microk8s.config > /tmp/microk8s.yaml
```

#### export the configurations
```
export KUBECONFIG=/tmp/microk8s.yaml
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
sudo snap remove microk8s
```

