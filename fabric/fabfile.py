from fabric import Connection, task

@task
def update_packages(ctx):
    """Updating packages"""
    print(f"Updating packages on {ctx.host}")
    ctx.sudo("sudo apt-get update -y && sudo apt-get upgrade -y")

@task
def disable_selinux_swap(ctx):
    """

    Disable SELinux so kubernetes can communicate with other hosts
    Disable Swap https://github.com/kubernetes/kubernetes/issues/53533
    """
    ctx.sudo("swapoff -a")
    ctx.sudo("sed -i 's/.* none.* swap.* sw.*/#&/' /etc/fstab")
 
@task
def install_additional_packages(ctx):
    """Install additional packages"""
    print(f"Installing additional packages on {ctx.host}")
    ctx.sudo("apt-get install curl")
    ctx.sudo("apt-get install wget")
    ctx.sudo("apt-get install apt-transport-https")
    ctx.sudo("apt-get install vim wget ca-certificates gnupg lsb-release")

@task
def enable_bridge_network(ctx):
    """Enable bridge network visible to kubernetes"""
    print(f"Enable bridge network")
    ctx.sudo("lsmod | grep br_netfilter")
    ctx.sudo("modprobe br_netfilter")
    ctx.sudo("sysctl net.bridge.bridge-nf-call-iptables=1")
    ctx.sudo("lsmod | grep br_netfilter")

@task
def install_docker(ctx):
    """Install Docker"""
    print(f"Installing Docker on {ctx.host}")
    ctx.sudo("wget -O - https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",shell=True)
    #ctx.sudo("curl -fsSL https://download.docker.com/linux/ubuntu/gpg > docker.gpg")
    #ctx.sudo("cat docker.gpg | gpg --batch --yes --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg", shell=True)
    print(f"Creating docker.list on {ctx.host}")
    ctx.sudo("echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",shell=True)
    print(f"update the packages on {ctx.host}")
    ctx.sudo("apt-get update -y")
    print(f"installing the Docker CE on {ctx.host}")
    ctx.sudo("apt-get install docker-ce -y --allow-change-held-packages")

    print(f"\ninstalling the Docker CLI on {ctx.host}")
    ctx.sudo("apt-get install docker-ce-cli -y --allow-change-held-packages")

    print(f"\ninstalling the ContainerD  on {ctx.host}")
    ctx.sudo("apt-get install containerd.io -y --allow-change-held-packages")
    ctx.sudo("mkdir -p /etc/docker")

    print(f"\ncreating the Docker config file on {ctx.host}")
    ctx.sudo("cat <<EOF | sudo tee /etc/docker/daemon.json { \"exec-opts\": [\"native.cgroupdriver=systemd\"], \"log-driver\": \"json-file\", \"log-opts\": { \"max-size\": \"100m\" }, \"storage-driver\": \"overlay2\" } EOF",shell=True)

    ctx.run("docker --version")
    print(f"\nRefreshing the services on {ctx.host}")
    ctx.sudo("systemctl enable docker.service")
    print(f"\nRestaring the services on {ctx.host}")
    ctx.sudo("systemctl restart docker.service")
    print(f"\nStatus of the services on {ctx.host}")
    ctx.sudo("systemctl status docker.service | cat")
    
   
@task
def install_kubernetes(ctx):
    """Install Kubernetes"""
    print(f"Installing Kubernetes on {ctx.host}")
    ctx.sudo("apt-get update && apt-get install -y apt-transport-https")
    ctx.sudo(
        "curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -"
    )
    ctx.sudo(
        'echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | \
          tee -a /etc/apt/sources.list.d/kubernetes.list && apt-get update'
    )
    ctx.sudo(
        "apt-get update && apt-get install -y kubelet kubeadm kubectl kubernetes-cni"
    )
    ctx.sudo("apt-mark hold kubelet kubeadm kubectl")
    ctx.sudo("ufw allow 6443")
    ctx.sudo("ufw allow 6443/tcp")
    
@task
def provision_clusters(ctx):
		"""Provision Clusters"""
		#for host in ["14a63d90ce1c.mylabserver.com"]:
		conn = Connection("14a63d90ce1c.mylabserver.com","cloud_user",connect_kwargs={"key_filename": "/home/govind/k8skey_rsa"})
		update_packages(conn)
		disable_selinux_swap(conn)
		install_additional_packages(conn)
		install_docker(conn)
		install_kubernetes(conn)
