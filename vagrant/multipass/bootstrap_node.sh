#!/bin/bash

# ip -f inet addr show enp0s1 | awk '/inet / {print $2}' |cut -f1 -d"/"
echo "[TASK 1] Join node to Kubernetes Cluster"
bash /mnt/share/joincluster.sh >/dev/null 2>&1
