#!/usr/bin/env python3
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本主要负责k8s集群安装前的相关准备工作

import copy
import os

from invocations.console import confirm

# 导入自定义工具库
# lib_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(lib_path)
from lib.remote import Remote
from lib.xmlFile import XmlFile
from lib.base import Base

class Prepare(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

        ips_data = self.config_object.get_node_by_attr("name", "ips")

        self.dockerSubnetIpRange = ips_data.find('dockerSubnetIpRange').text.replace("/", "\/")

    def __del__(self):
        pass

    #prepare works for every node
    def installNodeNormal(self, nodename):
        # 初始化远程工具对象
        robj = Remote(self.getEnv(nodename))

        cfsslBinPath = self.getLocalPath('cfsslBinPath')
        configPath = self.getLocalPath('configPath')
        remoteSysctlPath = self.getRemotePath('remoteSysctlPath')
        remoteLocalBinPath = self.getRemotePath('remoteLocalBinPath')
        # remoteSystemdPath = self.getRemotePath('remoteSystemdPath')

        # tmpPath = self.getLocalPath('tmpPath')
        # dockerConfigPath = self.getLocalPath('dockerConfigPath')

        #install some packages for proxy
        # cmdRemote = "yum install -y ipvsadm ipset conntrack"
        # cmdRemote = "yum install -y conntrack"
        # robj.sudo(cmdRemote)

        #upload cfssl file
        robj.upload(cfsslBinPath+"/cfssl", remoteLocalBinPath+"/")
        robj.upload(cfsslBinPath+"/cfssljson", remoteLocalBinPath+"/")
        robj.upload(cfsslBinPath+"/cfssl-certinfo", remoteLocalBinPath+"/")

        #cfssl tool
        if robj.checkpath(remoteLocalBinPath+"/cfssl") == True:
            print("ready to chmod cfssl ...")
            cmdRemote = "chmod +x /usr/local/bin/cfssl*"
            robj.sudo(cmdRemote)

        #close selinux
        print("ready to close selinux ...")
        robj.sudo("setenforce 0")
        robj.sudo("sed -i \"s/^SELINUX=enforcing/SELINUX=disabled/g\" /etc/sysconfig/selinux")
        robj.sudo("sed -i \"s/^SELINUX=enforcing/SELINUX=disabled/g\" /etc/selinux/config")
        robj.sudo("sed -i \"s/^SELINUX=permissive/SELINUX=disabled/g\" /etc/sysconfig/selinux")
        robj.sudo("sed -i \"s/^SELINUX=permissive/SELINUX=disabled/g\" /etc/selinux/config")
        robj.sudo("getenforce")
        #close swap
        print("ready to close swap ...")
        robj.sudo("swapoff -a")
        #comment swap line
        robj.sudo("sed -i 's/.*swap.*/#&/' /etc/fstab")
        robj.sudo("cat /etc/fstab")
        #config kernel
        print("ready to config kernel ...")
        robj.upload(configPath+"/sysctl/k8s.conf", remoteSysctlPath+"/")
        robj.sudo("modprobe br_netfilter")
        #reload system config
        print("reload system config ...")
        robj.sudo("sysctl -p "+remoteSysctlPath+"/k8s.conf")
        #close firewall 
        print("ready to stop firewall ...")
        robj.sudo("systemctl stop firewalld")
        robj.sudo("systemctl disable firewalld")
        robj.sudo("systemctl status firewalld")
        #remove old version of docker
        robj.sudo("systemctl stop docker")
        robj.sudo("yum remove -y docker docker-client docker-client-latest docker-common")
        robj.sudo("yum remove -y docker-latest docker-latest-logrotate docker-logrotate docker-engine")
        robj.sudo("systemctl status docker")
        # yum priorities plugin
        print("ready to install yum priorities plugin ...")
        robj.sudo("yum install -y yum-plugin-priorities")
        #epel-release
        print("ready to install epel repository ...")
        robj.sudo("yum install -y epel-release")
        robj.sudo("yum repolist")
        #ntpdate
        if self.mode=="dev":
            print("ready to install ntpdate ...")
            robj.sudo("yum -y install ntpdate")
            robj.sudo("systemctl enable ntpdate")
            robj.sudo("systemctl restart ntpdate")

        #set prioritiy for epel
        if robj.checkpath("/etc/yum.repos.d/epel.repo") == True:
            cmdRemote = "grep -c \"priority=\" /etc/yum.repos.d/epel.repo"
            robj.sudo(cmdRemote)
            priorityExists = robj.getResult().stdout.rstrip()
            if priorityExists == '0':
                # insert priority field under the 'enabled=' line
                cmdRemote = "sed -i '/enabled=/a\priority=1' /etc/yum.repos.d/epel.repo"
                robj.sudo(cmdRemote)
                
        # update yum
        cmdRemote = "yum makecache"
        robj.sudo(cmdRemote)

        # cmdRemote = "yum update -y"
        # robj.sudo(cmdRemote)

        cmdRemote = "yum install -y deltarpm" 
        robj.sudo(cmdRemote)

        # cmdRemote = "yum update -y"
        # robj.sudo(cmdRemote)

        #wget tool
        print("ready to install wget ..."    )
        cmdRemote = "yum install -y wget"
        robj.sudo(cmdRemote)

        #net tool
        print("ready to install net-tools ...")
        cmdRemote = "yum install -y net-tools"
        robj.sudo(cmdRemote)

        #install docker component
        if robj.checkpath("/usr/bin/docker") == False:
            #Set up repository
            print("ready to install docker-ce ...")

            #install required packages. yum-utils provides the yum-config-manager utility, 
            # and device-mapper-persistent-data and lvm2 are required by the devicemapper storage driver
            cmdRemote = "yum install -y yum-utils device-mapper-persistent-data lvm2"
            robj.sudo(cmdRemote)
            #set up the stable repository
            # sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            cmdRemote = "yum-config-manager --add-repo"
            cmdRemote = cmdRemote + " http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo"
            robj.sudo(cmdRemote)

            # update yum
            cmdRemote = "yum makecache"
            robj.sudo(cmdRemote)
            # cmdRemote = "yum update -y"
            # robj.sudo(cmdRemote)

            #List and sort the versions available in your repo. This example sorts results by version number, highest to lowest, and is truncated
            print("list docker versions ...")
            cmdRemote = "yum list docker-ce --showduplicates | sort -r"
            robj.sudo(cmdRemote)

            robj.sudo("sleep 5")

            # if not confirm("Ready to install docker-ce-18.06.3.ce, Continue[Y/N]?"):
                # return True

            #Install a specific version by its fully qualified package name
            print("ready to install docker-ce-18.06.3.ce ...")
            cmdRemote = "yum install -y docker-ce-18.06.3.ce docker-ce-cli-18.06.3.ce containerd.io"
            robj.sudo(cmdRemote)

        #set docker to start when the system is booted
        cmdRemote = "systemctl enable docker"
        robj.sudo(cmdRemote)
        #set subnet for docker

        # upload docker service file
        # sedRegex = "sed \"s/{dockerSubnetIpRange}/%s/g\"" % self.dockerSubnetIpRange

        # file_tmp = tmpPath + "/docker.service"
        # file_config = dockerConfigPath + "/docker.service"
        # cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        # robj.local(cmd_local)

        # 上传文件到远程主机
        # robj.upload(file_tmp, remoteSystemdPath+"/", True)

        #reload daemon
        cmdRemote = "systemctl daemon-reload"
        robj.sudo(cmdRemote)
        #start docker
        cmdRemote = "systemctl restart docker"
        robj.sudo(cmdRemote)
        # check docker status
        print("check docker-ce status ...")
        cmdRemote = "systemctl status docker"
        robj.sudo(cmdRemote)

        # check subnet of docker
        print("check subnet of docker0 ...")
        cmdRemote = "ip addr show docker0"
        robj.sudo(cmdRemote)

        #install socat
        cmdRemote = "yum install -y socat"
        robj.sudo(cmdRemote)

        #prepare deployment directory
        cmdRemote = "mkdir -p /opt/kubernetes/{bin,cfg,ssl,log}"
        robj.sudo(cmdRemote)
        #set environment variable
        robj.upload(configPath+"/sysctl/k8s.sh", "/etc/profile.d/", True)
        # cmdRemote = "echo 'export PATH=/opt/kubernetes/bin:$PATH' > /etc/profile.d/k8s.sh"
        # robj.sudo(cmdRemote)
        robj.sudo("chmod 755 /etc/profile.d/k8s.sh")
        cmdRemote = "source /etc/profile.d/k8s.sh"
        robj.run(cmdRemote)

        
    

