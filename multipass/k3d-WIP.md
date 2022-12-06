# Microk8s

#### Create a new Ubuntu VM
```
multipass launch --name k3s --mem 8G
```

#### Install microk8s in the VM
```
multipass exec k3s -- sudo apt update -y && curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash 
```
#### copy the cluster configuration
```
multipass exec k3s -- sudo k3d cluster create mycluster
```

#### copy the cluster configuration
```
multipass exec k3s -- sudo cat /etc/rancher/k3s/k3s.yaml > /tmp/k3s.yaml
```

#### export the configurations
```
export KUBECONFIG=/tmp/k3s.yaml
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
multipass delete k3s && multipass purge
```
