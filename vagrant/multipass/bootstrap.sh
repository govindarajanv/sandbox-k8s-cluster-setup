#!/bin/bash


#Update and upgrade Ubuntu OS
echo "[TASK 0] Update the packages"
apt-get update -y && apt-get upgrade -y

#Disable swap Kubernetes will give you errors and warnings
echo "[TASK 1] Disabling swap"
swapoff -a
#vim /etc/fstab
sed -i 's/.* none.* swap.* sw.*/#&/' /etc/fstab
#sudo sed -i '/.* none.* swap.* sw.*/s/^#//' /etc/fstab
cat /etc/fstab

#Install required packages
echo "[TASK 2] Install the required packages"
sudo apt-get install curl apt-transport-https vim wget ca-certificates gnupg lsb-release -y

#Enable bride network visible to kubernetes 
echo "[TASK 3] Enable bridge network"
lsmod | grep br_netfilter
modprobe br_netfilter
sysctl net.bridge.bridge-nf-call-iptables=1
lsmod | grep br_netfilter

#Docker Installation and configuration
echo "[TASK 4] Docker installation"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

mkdir -p /etc/docker

cat <<EOF | sudo tee /etc/docker/daemon.json
{ "exec-opts": ["native.cgroupdriver=systemd"],
"log-driver": "json-file",
"log-opts":
{ "max-size": "100m" },
"storage-driver": "overlay2"
}
EOF

echo "[TASK 5] Start Docker Daemon"
systemctl enable docker
systemctl restart docker
systemctl status docker | cat

echo "[TASK 6] Start Containerd Daemon"
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
systemctl restart containerd

#Kubernetes k8s Installation
echo "[TASK 7] kubernetes installation"
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
apt-get update -y 
apt-get install kubectl kubeadm kubelet kubernetes-cni -y

#Enable Firewall to allow K8S API port
echo "[TASK 8] Enable Firewall"
sudo ufw allow 6443
sudo ufw allow 6443/tcp
