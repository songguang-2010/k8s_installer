#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

# load config items
# . ${filePath}/config_var.sh

# #close selinux
# echo "ready to close selinux ..."
# setenforce 0
# sed -i "s/^SELINUX=enforcing/SELINUX=disabled/g" /etc/sysconfig/selinux 
# sed -i "s/^SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config 
# sed -i "s/^SELINUX=permissive/SELINUX=disabled/g" /etc/sysconfig/selinux 
# sed -i "s/^SELINUX=permissive/SELINUX=disabled/g" /etc/selinux/config 
# getenforce

# #close swap
# swapoff -a
# #comment swap line
# sed -i 's/.*swap.*/#&/' /etc/fstab
# cat /etc/fstab

# #config kernel
# cat <<EOF >  /etc/sysctl.d/k8s.conf
# net.bridge.bridge-nf-call-ip6tables = 1
# net.bridge.bridge-nf-call-iptables = 1
# EOF
# modprobe br_netfilter
# #reload system config
# sysctl -p /etc/sysctl.d/k8s.conf

# #close firewall 
# echo "ready to stop firewall ..."
# systemctl stop firewalld
# systemctl disable firewalld
# echo "check firewall status ..."
# systemctl status firewalld

# #remove old version 
# systemctl stop docker
# echo "ready to remove current docker ..."
# yum remove -y docker docker-client docker-client-latest docker-common
# yum remove -y docker-latest docker-latest-logrotate docker-logrotate docker-engine
# echo "check docker status ..."
# systemctl status docker 

# # yum priorities plugin
# echo "ready to install yum priorities plugin ..."
# yum install -y yum-plugin-priorities

# #epel-release
# echo "ready to install epel repository ..."
# yum install -y epel-release
# echo "check epel repository ..."
# yum repolist

# #set prioritiy for epel
# priorityExists=$(grep -c "priority=" /etc/yum.repos.d/epel.repo)
# if [ $priorityExists -eq '0' ]; then
#     # insert priority field under the 'enabled=' line
#     sed -i '/enabled=/a\priority=1' /etc/yum.repos.d/epel.repo
# fi

# # update yum
# yum makecache
# yum update -y

#ntpdate
# echo "ready to install ntpdate ..."
# yum -y install ntpdate
# systemctl enable ntpdate
# systemctl restart ntpdate

# #wget tool
# echo "ready to install wget ..."
# yum install -y wget

# #net tool
# echo "ready to install net-tools ..."
# yum install -y net-tools

# #install docker component
# if [ ! -f "/usr/bin/docker" ]; then
#     #Set up repository
#     echo "ready to install docker-ce ..."
    
#     #install required packages. yum-utils provides the yum-config-manager utility, and device-mapper-persistent-data and lvm2 are required by the devicemapper storage driver
#     yum install -y yum-utils device-mapper-persistent-data lvm2
#     #set up the stable repository
#     # sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
#     yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    
#     # update yum
#     yum makecache
#     yum update -y

#     #List and sort the versions available in your repo. This example sorts results by version number, highest to lowest, and is truncated
#     yum list docker-ce --showduplicates | sort -r
#     #Install a specific version by its fully qualified package name
#     yum install -y docker-ce-18.06.3.ce docker-ce-cli-18.06.3.ce containerd.io
# fi

# #set docker to start when the system is booted
# systemctl enable docker
# #start docker
# systemctl restart docker
# # check docker status
# echo "check docker-ce status ..."
# systemctl status docker

# #install socat
# yum install -y socat

# #prepare deployment directory
# mkdir -p /opt/kubernetes/{bin,cfg,ssl,log}
# #set environment variable
# echo 'export PATH=/opt/kubernetes/bin:$PATH' > /etc/profile.d/k8s.sh
# source /etc/profile.d/k8s.sh

# #cfssl tool
# if [ -f "/usr/local/bin/cfssl" ]; then
#     chmod +x /usr/local/bin/cfssl*
# fi

