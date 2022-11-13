#!/bin/bash

echo "[TASK 1] Initialize Kubernetes Cluster"
kubeadm init --pod-network-cidr=10.244.0.0/16 >> /root/kubeinit.log 2>/dev/null

echo "[TASK 2] Initialize Kubernetes Cluster"
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
mkdir -p /home/vagrant/.kube
cp -i /etc/kubernetes/admin.conf /home/vagrant/.kube/config
chown vagrant:vagrant /home/vagrant/.kube/config

echo "[TASK 3] Deploy Flannel network"
kubectl --kubeconfig=/etc/kubernetes/admin.conf create -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml >/dev/null 2>&1

echo "[TASK 4] Generate and save cluster join command to /joincluster.sh"
kubeadm token create --print-join-command > /mnt/share/joincluster.sh 2>/dev/null
ip_addr=$(ip -f inet addr show enp0s1 | awk '/inet / {print $2}' |cut -f1 -d"/")
echo $ip_addr > /mnt/share/master.data
