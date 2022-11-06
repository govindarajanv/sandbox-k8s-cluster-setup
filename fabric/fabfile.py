from fabric import Connection, task

@task
def install_docker(ctx):
    """Install Docker"""
    print(f"Installing Docker on {ctx.host}")
    ctx.sudo("apt-get update && apt-get install -qy docker.io")
    ctx.run("docker --version")
    ctx.sudo("systemctl enable docker.service")
    
@task
def disable_selinux_swap(ctx):
    """
    Disable SELinux so kubernetes can communicate with other hosts
    Disable Swap https://github.com/kubernetes/kubernetes/issues/53533
    """
    ctx.sudo('sed -i "/ swap / s/^/#/" /etc/fstab')
    ctx.sudo("swapoff -a")
    
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
        "apt-get update && apt-get install -y kubelet=1.21.1-00 kubeadm=1.21.1-00 kubectl=1.21.1-00"
    )
    ctx.sudo("apt-mark hold kubelet kubeadm kubectl")
    
@task
def provision_machines(ctx):
    for conn in get_connections(hosts):
        install_docker(conn)
        disable_selinux_swap(conn)
        install_kubernetes(conn)
