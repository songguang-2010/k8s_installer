#!/usr/bin/env python3
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本主要负责k8s集群安装前的相关准备工作

import copy
import os
import base64
import csv
import sys

# 导入自定义工具库
# lib_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(lib_path)
from lib.remote import Remote
from lib.xmlFile import XmlFile
from lib.base import Base

class Kbs(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

        ips_data = self.config_object.get_node_by_attr("name", "ips")

        self.serviceClusterIpRange = ips_data.find('serviceClusterIpRange').text.replace("/", "\/")
        self.serviceClusterGatewayIp = ips_data.find('serviceClusterGatewayIp').text
        self.serviceClusterDnsIp = ips_data.find('serviceClusterDnsIp').text
        self.podClusterIpRange = ips_data.find('podClusterIpRange').text.replace("/", "\/")

        node_data = self.node_object.get_node_by_attr("name", "proxy")
        self.proxy_host = node_data.find('hostname').text
        self.proxy_port = node_data.find('port').text

    def __del__(self):
        pass

    #before install kbs master
    def installKbsMasterBefore(self):
        node_env1 = self.getEnv("master1")
        # 初始化远程工具对象
        robj_master1 = Remote(node_env1)

        remoteSslPath = self.getRemotePath('remoteSslPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')
        remoteLocalBinPath = self.getRemotePath('remoteLocalBinPath')

        tmpPath = self.getLocalPath('tmpPath')
        etcdConfigPath = self.getLocalPath('etcdConfigPath')
        kbsConfigPath = self.getLocalPath('kbsConfigPath')

        #download ca files form master1 to local
        robj_master1.download(remoteSslPath+"/ca.csr", tmpPath+"/")
        # robj_master1.download(remoteSslPath+"/ca.pem", tmpPath+"/")
        # robj_master1.download(remoteSslPath+"/ca-key.pem", tmpPath+"/")

        #upload ca cert files
        # robj_master1.upload(tmpPath+"/ca.pem", remoteSslPath+"/")
        # robj_master1.upload(tmpPath+"/ca-key.pem", remoteSslPath+"/")

        #upload files
        robj_master1.upload(etcdConfigPath+"/ca-config.json", remoteSslPath+"/")

        # upload kubernetes csr config file
        file_tmp = tmpPath + "/kubernetes-csr.json"
        file_config = kbsConfigPath + "/kubernetes-csr.json"
        sedRegex = "sed \"s/{kbsMasterIp1}/%s/g\"" % self.getEnv("master1").host
        sedRegex = sedRegex + " | sed \"s/{kbsMasterIp2}/%s/g\"" % self.getEnv("master2").host
        sedRegex = sedRegex + " | sed \"s/{kbsMasterIp3}/%s/g\"" % self.getEnv("master3").host
        sedRegex = sedRegex + " | sed \"s/{kbsMasterProxyIp}/%s/g\"" % self.proxy_host
        sedRegex = sedRegex + " | sed \"s/{serviceClusterGatewayIp}/%s/g\"" % self.serviceClusterGatewayIp
        sedRegex = sedRegex + " | sed \"s/{workerNodeIp}/%s/g\"" % self.getEnv("node1").host
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj_master1.local(cmd_local)
        # 上传文件到远程主机
        robj_master1.upload(file_tmp, remoteSslPath+"/")

        # robj_master1.upload(kbsConfigPath+"/admin-csr.json", remoteSslPath+"/")

        #create token.csv file for bootstrap authority in master1
        print("ready to create tocken.csv file in master1 ...")
        cmdRemote = "/bin/sh -c \'BOOTSTRAP_TOKEN=$(head -c 16 /dev/urandom | od -An -t x | tr -d \" \")"
        cmdRemote = cmdRemote + "; BOOTSTRAP_CONTENT=\"${BOOTSTRAP_TOKEN},kubelet-bootstrap,10001,\\\"system:kubelet-bootstrap\\\"\""
        cmdRemote= cmdRemote + "; echo ${BOOTSTRAP_CONTENT} > "+remoteCfgPath+"/token.csv\'"
        # print(cmdRemote)
        robj_master1.sudo(cmdRemote)
        robj_master1.sudo("cat "+remoteCfgPath+"/token.csv")

        #create kubernetes cert files in master1
        print("ready to create kubernetes cert file in master1 ...")
        cmdRemote = remoteLocalBinPath+"/cfssl gencert"
        cmdRemote = cmdRemote + " -ca="+remoteSslPath+"/ca.pem"
        cmdRemote = cmdRemote + " -ca-key="+remoteSslPath+"/ca-key.pem"
        cmdRemote = cmdRemote + " -config="+remoteSslPath+"/ca-config.json"
        cmdRemote = cmdRemote + " -profile=kubernetes "+remoteSslPath+"/kubernetes-csr.json"
        cmdRemote = cmdRemote + " | "+remoteLocalBinPath+"/cfssljson -bare "+remoteSslPath+"/kubernetes"
        robj_master1.sudo(cmdRemote)

        #create metrics api aggregator cert files in master1
        robj_master1.upload(kbsConfigPath+"/front-proxy-ca-csr.json", remoteSslPath+"/")
        robj_master1.upload(kbsConfigPath+"/front-proxy-client-csr.json", remoteSslPath+"/", True)
        # generate ca root cert
        cmdRemote = remoteLocalBinPath+"/cfssl gencert -initca "+remoteSslPath+"/front-proxy-ca-csr.json"
        cmdRemote = cmdRemote + " | "+remoteLocalBinPath+"/cfssljson -bare "+remoteSslPath+"/front-proxy-ca"
        robj_master1.sudo(cmdRemote)
        # generate client cert for each node
        cmdRemote = remoteLocalBinPath+"/cfssl gencert -ca="+remoteSslPath+"/front-proxy-ca.pem"
        cmdRemote = cmdRemote + " -ca-key="+remoteSslPath+"/front-proxy-ca-key.pem"
        cmdRemote = cmdRemote + " -config="+remoteSslPath+"/ca-config.json"
        cmdRemote = cmdRemote + " -profile=kubernetes "+remoteSslPath+"/front-proxy-client-csr.json"
        cmdRemote = cmdRemote + " | "+remoteLocalBinPath+"/cfssljson -bare "+remoteSslPath+"/front-proxy-client"
        robj_master1.sudo(cmdRemote)

        # #create kubectl cert files in master1
        # cmdRemote = "/usr/local/bin/cfssl gencert"
        # cmdRemote = cmdRemote + " -ca="+remoteSslPath+"/ca.pem"
        # cmdRemote = cmdRemote + " -ca-key="+remoteSslPath+"/ca-key.pem"
        # cmdRemote = cmdRemote + " -config="+remoteSslPath+"/ca-config.json"
        # cmdRemote = cmdRemote + " -profile=kubernetes "+remoteSslPath+"/admin-csr.json"
        # cmdRemote = cmdRemote + " | /usr/local/bin/cfssljson -bare "+remoteSslPath+"/admin"
        # robj_master1.sudo(cmdRemote)

    #after install kbs master
    # def installKbsMasterAfter(self):
        # node_env1 = self.getEnv("master1")
        # 初始化远程工具对象
        # robj_master1 = Remote(node_env1)

        # remoteBinPath = self.getRemotePath('remoteBinPath')
        # remoteSslPath = self.getRemotePath('remoteSslPath')

        # kbsBinPath = self.getLocalPath('kbsBinPath')
        # kbsConfigPath = self.getLocalPath('kbsConfigPath')
        # tmpPath = self.getLocalPath('tmpPath')

        # robj_master1.upload(kbsConfigPath+"/admin-csr.json", remoteSslPath+"/")

        # #create kubectl cert files in master1
        # cmdRemote = "/usr/local/bin/cfssl gencert"
        # cmdRemote = cmdRemote + " -ca="+remoteSslPath+"/ca.pem"
        # cmdRemote = cmdRemote + " -ca-key="+remoteSslPath+"/ca-key.pem"
        # cmdRemote = cmdRemote + " -config="+remoteSslPath+"/ca-config.json"
        # cmdRemote = cmdRemote + " -profile=kubernetes "+remoteSslPath+"/admin-csr.json"
        # cmdRemote = cmdRemote + " | /usr/local/bin/cfssljson -bare "+remoteSslPath+"/admin"
        # robj_master1.sudo(cmdRemote)

        #upload binary files to master node
        # if robj_master1.checkpath((remoteBinPath+"/kubectl")) == False:
        #     robj_master1.upload((kbsBinPath+"/kubectl"), (remoteBinPath+"/"))

        #set cluster parameters
        # cmdRemote = remoteBinPath + "/kubectl config set-cluster kubernetes"
        # cmdRemote = cmdRemote + " --certificate-authority="+remoteSslPath+"/ca.pem"
        # cmdRemote = cmdRemote + " --embed-certs=true"
        # cmdRemote = cmdRemote + " --server=https://"+self.proxy_host+":"+self.proxy_port
        # robj_master1.sudo(cmdRemote)

        #set client authority parameters
        # cmdRemote = remoteBinPath + "/kubectl config set-credentials admin"
        # cmdRemote = cmdRemote + " --client-certificate="+remoteSslPath+"/admin.pem"
        # cmdRemote = cmdRemote + " --embed-certs=true"
        # cmdRemote = cmdRemote + " --client-key="+remoteSslPath+"/admin-key.pem"
        # robj_master1.sudo(cmdRemote)

        #set context parameters
        # cmdRemote = remoteBinPath + "/kubectl config set-context kubernetes"
        # cmdRemote = cmdRemote + " --cluster=kubernetes"
        # cmdRemote = cmdRemote + " --user=admin"
        # robj_master1.sudo(cmdRemote)

        #set default context
        # cmdRemote = remoteBinPath + "/kubectl config use-context kubernetes"
        # robj_master1.sudo(cmdRemote)

    # install kubectl to node
    def installKubectl(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        master1_env = self.getEnv("master1")
        # 初始化远程工具对象
        robj_master1 = Remote(master1_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remoteSslPath = self.getRemotePath('remoteSslPath')

        tmpPath = self.getLocalPath('tmpPath')
        kbsBinPath = self.getLocalPath('kbsBinPath')
        kbsConfigPath = self.getLocalPath('kbsConfigPath')

        robj_master1.upload(kbsConfigPath+"/admin-csr.json", remoteSslPath+"/")

        #create kubectl cert files in master1
        cmdRemote = "/usr/local/bin/cfssl gencert"
        cmdRemote = cmdRemote + " -ca="+remoteSslPath+"/ca.pem"
        cmdRemote = cmdRemote + " -ca-key="+remoteSslPath+"/ca-key.pem"
        cmdRemote = cmdRemote + " -config="+remoteSslPath+"/ca-config.json"
        cmdRemote = cmdRemote + " -profile=kubernetes "+remoteSslPath+"/admin-csr.json"
        cmdRemote = cmdRemote + " | /usr/local/bin/cfssljson -bare "+remoteSslPath+"/admin"
        robj_master1.sudo(cmdRemote)

        #download binary files to local
        # robj_master1.download(remoteBinPath+"/kubectl", tmpPath+"/")

        #download ca files from master1 to local
        robj_master1.download(remoteSslPath+"/ca.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca-key.pem", tmpPath+"/")

        #download kubectl ca files from master1 to local
        robj_master1.download(remoteSslPath+"/admin.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/admin.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/admin-key.pem", tmpPath+"/")

        # upload kubectl file
        if robj_admin.checkpath(remoteBinPath+"/kubectl") == False:
            robj_admin.upload(kbsBinPath+"/kubectl", remoteBinPath+"/")

        #upload cert files to master node
        robj_admin.upload(tmpPath+"/ca.pem", remoteSslPath+"/")
        robj_admin.upload(tmpPath+"/admin.pem", remoteSslPath+"/")
        robj_admin.upload(tmpPath+"/admin-key.pem", remoteSslPath+"/")

        #set cluster parameters
        cmdRemote = remoteBinPath + "/kubectl config set-cluster kubernetes"
        cmdRemote = cmdRemote + " --certificate-authority="+remoteSslPath+"/ca.pem"
        cmdRemote = cmdRemote + " --embed-certs=true"
        cmdRemote = cmdRemote + " --server=https://"+self.proxy_host+":"+self.proxy_port
        robj_admin.sudo(cmdRemote)

        #set client authority parameters
        cmdRemote = remoteBinPath + "/kubectl config set-credentials admin"
        cmdRemote = cmdRemote + " --client-certificate="+remoteSslPath+"/admin.pem"
        cmdRemote = cmdRemote + " --embed-certs=true"
        cmdRemote = cmdRemote + " --client-key="+remoteSslPath+"/admin-key.pem"
        robj_admin.sudo(cmdRemote)

        #set context parameters
        cmdRemote = remoteBinPath + "/kubectl config set-context kubernetes"
        cmdRemote = cmdRemote + " --cluster=kubernetes"
        cmdRemote = cmdRemote + " --user=admin"
        robj_admin.sudo(cmdRemote)

        #set default context
        cmdRemote = remoteBinPath + "/kubectl config use-context kubernetes"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl get nodes -o wide"
        robj_admin.sudo(cmdRemote)


    #install kbs master normal
    def installKbsMasterNormal(self, nodename):
        node_env = self.getEnv(nodename)
        # 初始化远程工具对象
        robj = Remote(node_env)

        node_env1 = self.getEnv("master1")
        # 初始化远程工具对象
        robj_master1 = Remote(node_env1)

        remoteSslPath = self.getRemotePath('remoteSslPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')
        remoteSystemdPath = self.getRemotePath('remoteSystemdPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        tmpPath = self.getLocalPath('tmpPath')
        kbsConfigPath = self.getLocalPath('kbsConfigPath')
        kbsBinPath = self.getLocalPath('kbsBinPath')

        #stop relative service if the service is running
        robj.sudo("systemctl stop kube-apiserver")
        robj.sudo("systemctl stop kube-controller-manager")
        robj.sudo("systemctl stop kube-scheduler")

        #install some packages for proxy
        cmdRemote = "yum install -y ipvsadm ipset conntrack"
        robj.sudo(cmdRemote)

        #download ca files from master1 to local
        robj_master1.download(remoteSslPath+"/ca.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca-key.pem", tmpPath+"/")
        
        #download etcd ca files from master1 to local
        robj_master1.download(remoteSslPath+"/etcd.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/etcd.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/etcd-key.pem", tmpPath+"/")

        #download kubernetes ca files from master1 to local
        robj_master1.download(remoteSslPath+"/kubernetes.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/kubernetes.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/kubernetes-key.pem", tmpPath+"/")

        #download metrics api ca files from master1 to local
        robj_master1.download(remoteSslPath+"/front-proxy-ca.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/front-proxy-client.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/front-proxy-client.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/front-proxy-client-key.pem", tmpPath+"/")

        #download token csv file from master1 to local
        robj_master1.download(remoteCfgPath+"/token.csv", tmpPath+"/")

        #upload ca files to master node
        robj.upload(tmpPath+"/ca.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/ca.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/ca-key.pem", remoteSslPath+"/")

        robj.upload(tmpPath+"/etcd.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/etcd.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/etcd-key.pem", remoteSslPath+"/")

        robj.upload(tmpPath+"/kubernetes.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/kubernetes.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/kubernetes-key.pem", remoteSslPath+"/")

        robj.upload(tmpPath+"/front-proxy-ca.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/front-proxy-client.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/front-proxy-client.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/front-proxy-client-key.pem", remoteSslPath+"/")

        robj.upload(tmpPath+"/token.csv", remoteCfgPath+"/")
        
        #upload binary files to master node
        robj.upload((kbsBinPath+"/kube-apiserver"), (remoteBinPath+"/"))
        robj.upload((kbsBinPath+"/kube-controller-manager"), (remoteBinPath+"/"))   
        robj.upload((kbsBinPath+"/kube-scheduler"), (remoteBinPath+"/"))

        #upload kubernetes api server config file
        file_tmp = tmpPath + "/kube-apiserver.conf"
        file_config = kbsConfigPath + "/kube-apiserver.conf"
        sedRegex = "sed \"s/^--advertise-address={nodeIp}/--advertise-address=%s/g\"" % node_env.host
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp1}/%s/g\"" % self.getEnv("master1").host
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp2}/%s/g\"" % self.getEnv("master2").host
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp3}/%s/g\"" % self.getEnv("master3").host
        sedRegex = sedRegex + " | sed \"s/{serviceClusterIpRange}/%s/g\"" % self.serviceClusterIpRange
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj.local(cmd_local)
        # 上传文件到远程主机
        robj.upload(file_tmp, remoteCfgPath+"/", True)

        # upload kubernetes controller manager config file
        file_tmp = tmpPath + "/kube-controller-manager.conf"
        file_config = kbsConfigPath + "/kube-controller-manager.conf"
        sedRegex = "sed \"s/{serviceClusterIpRange}/%s/g\"" % self.serviceClusterIpRange
        sedRegex = sedRegex + " | sed \"s/{podClusterIpRange}/%s/g\"" % self.podClusterIpRange
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj.local(cmd_local)
        # 上传文件到远程主机
        robj.upload(file_tmp, remoteCfgPath+"/", True)

        # upload kubernetes scheduler config file
        robj.upload(kbsConfigPath + "/kube-scheduler.conf", remoteCfgPath+"/", True)

        #upload systemd service file to master node
        robj.upload(kbsConfigPath + "/kube-apiserver.service", remoteSystemdPath+"/", True)
        robj.upload(kbsConfigPath + "/kube-controller-manager.service", remoteSystemdPath+"/", True)
        robj.upload(kbsConfigPath + "/kube-scheduler.service", remoteSystemdPath+"/", True)

        robj.sudo("systemctl daemon-reload")
        robj.sudo("systemctl enable kube-apiserver")
        robj.sudo("systemctl restart kube-apiserver")
        robj.sudo("systemctl status kube-apiserver")
        robj.sudo("systemctl enable kube-controller-manager")
        robj.sudo("systemctl restart kube-controller-manager")
        robj.sudo("systemctl status kube-controller-manager")
        robj.sudo("systemctl enable kube-scheduler")
        robj.sudo("systemctl restart kube-scheduler")
        robj.sudo("systemctl status kube-scheduler")

    #valid kbs master
    def validKbsMaster(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')

        # 在远端主机执行命令
        print("show apiserver info in port 6443: ")
        cmdRemote = "curl -L --cacert /opt/kubernetes/ssl/ca.pem"
        cmdRemote = cmdRemote + " https://"+self.proxy_host+":"+self.proxy_port+"/api"
        robj_admin.sudo(cmdRemote)

        # print("show apiserver info in port 8080: ")
        # cmdValid="curl -L http://"+proxy_host+":8080/api"
        # robj_admin.sudo(cmdValid)

        print("show cluster info by kubectl: ")
        cmdValid = remoteBinPath + "/kubectl get cs"
        robj_admin.sudo(cmdValid)

    #before install kbs node
    def installKbsNodeBefore(self):

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remoteSslPath = self.getRemotePath('remoteSslPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')
        remoteLocalBinPath = self.getRemotePath('remoteLocalBinPath')

        tmpPath = self.getLocalPath('tmpPath')
        kbsConfigPath = self.getLocalPath('kbsConfigPath')

        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        node_env1 = self.getEnv("master1")
        # 初始化远程工具对象
        robj_master1 = Remote(node_env1)

        #download token csv file from master1 to local
        robj_master1.download(remoteCfgPath+"/token.csv", tmpPath+"/")

        #####for kubelet#####

        #delete old role binding in master1
        cmdRemote = remoteBinPath + "/kubectl delete clusterrolebinding/kubelet-bootstrap"
        robj_admin.sudo(cmdRemote)

        #create role binding in master1
        cmdRemote = remoteBinPath + "/kubectl create clusterrolebinding kubelet-bootstrap"
        cmdRemote = cmdRemote + " --clusterrole=system:node-bootstrapper"
        cmdRemote = cmdRemote + " --user=kubelet-bootstrap"
        robj_admin.sudo(cmdRemote)

        #set cluster parameters and create kubelet bootstrapping kubeconfig file
        cmdRemote = remoteBinPath + "/kubectl config set-cluster kubernetes"
        cmdRemote = cmdRemote + " --certificate-authority="+remoteSslPath+"/ca.pem"
        cmdRemote = cmdRemote + " --embed-certs=true"
        cmdRemote = cmdRemote + " --server=https://"+self.proxy_host+":"+self.proxy_port
        cmdRemote = cmdRemote + " --kubeconfig="+remoteCfgPath+"/bootstrap.kubeconfig"
        robj_admin.sudo(cmdRemote)

        robj_admin.local("sleep 3")

        f = open(tmpPath+'/token.csv', 'r')
        csv_file = csv.reader(f)
        csv_content = next(csv_file)
        csv_token = csv_content[0]  
        f.close()

        #create authority parameters for client
        cmdRemote = remoteBinPath + "/kubectl config set-credentials kubelet-bootstrap"
        cmdRemote = cmdRemote + " --token=" + csv_token
        cmdRemote = cmdRemote + " --kubeconfig="+remoteCfgPath+"/bootstrap.kubeconfig"
        robj_admin.sudo(cmdRemote)

        #set context parameters
        cmdRemote = remoteBinPath + "/kubectl config set-context kubernetes"
        cmdRemote = cmdRemote + " --cluster=kubernetes"
        cmdRemote = cmdRemote + " --user=kubelet-bootstrap"
        cmdRemote = cmdRemote + " --kubeconfig="+remoteCfgPath+"/bootstrap.kubeconfig"
        robj_admin.sudo(cmdRemote)

        #set default context
        cmdRemote = remoteBinPath + "/kubectl config use-context kubernetes"
        cmdRemote = cmdRemote + " --kubeconfig="+remoteCfgPath+"/bootstrap.kubeconfig"
        robj_admin.sudo(cmdRemote)

        #####for proxy#####

        #upload proxy csr file to master1
        robj_master1.upload(kbsConfigPath+"/kube-proxy-csr.json", remoteSslPath+"/")

        #delete old proxy cert files in master1
        robj_master1.rmfile(remoteSslPath+"/kube-proxy.csr")
        robj_master1.rmfile(remoteSslPath+"/kube-proxy.pem")
        robj_master1.rmfile(remoteSslPath+"/kube-proxy-key.pem")

        #create proxy cert files in master1
        cmdRemote = "/usr/local/bin/cfssl gencert"
        cmdRemote = cmdRemote + " -ca="+remoteSslPath+"/ca.pem"
        cmdRemote = cmdRemote + " -ca-key="+remoteSslPath+"/ca-key.pem"
        cmdRemote = cmdRemote + " -config="+remoteSslPath+"/ca-config.json"
        cmdRemote = cmdRemote + " -profile=kubernetes "+remoteSslPath+"/kube-proxy-csr.json"
        cmdRemote = cmdRemote + " | "+remoteLocalBinPath+"/cfssljson -bare "+remoteSslPath+"/kube-proxy"
        robj_master1.sudo(cmdRemote)

        #download cert files from master1 to local
        robj_master1.download(remoteSslPath+"/kube-proxy.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/kube-proxy-key.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca.pem", tmpPath+"/")

        #upload cert files from local to admin node
        robj_admin.upload(tmpPath+"/kube-proxy.pem", remoteSslPath+"/")
        robj_admin.upload(tmpPath+"/kube-proxy-key.pem", remoteSslPath+"/")
        robj_admin.upload(tmpPath+"/ca.pem", remoteSslPath+"/")

        #create kube-proxy kubeconfig file in admin node
        cmdRemote = remoteBinPath + "/kubectl config set-cluster kubernetes"
        cmdRemote = cmdRemote + " --certificate-authority="+remoteSslPath+"/ca.pem"
        cmdRemote = cmdRemote + " --embed-certs=true"
        cmdRemote = cmdRemote + " --server=https://"+self.proxy_host+":"+self.proxy_port
        cmdRemote = cmdRemote + " --kubeconfig="+remoteCfgPath+"/kube-proxy.kubeconfig"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl config set-credentials kube-proxy"
        cmdRemote = cmdRemote + " --client-certificate="+remoteSslPath+"/kube-proxy.pem"
        cmdRemote = cmdRemote + " --client-key="+remoteSslPath+"/kube-proxy-key.pem"
        cmdRemote = cmdRemote + " --embed-certs=true"
        cmdRemote = cmdRemote + " --kubeconfig="+remoteCfgPath+"/kube-proxy.kubeconfig"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl config set-context kubernetes"
        cmdRemote = cmdRemote + " --cluster=kubernetes"
        cmdRemote = cmdRemote + " --user=kube-proxy"
        cmdRemote = cmdRemote + " --kubeconfig="+remoteCfgPath+"/kube-proxy.kubeconfig"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl config use-context kubernetes"
        cmdRemote = cmdRemote + " --kubeconfig="+remoteCfgPath+"/kube-proxy.kubeconfig"
        robj_admin.sudo(cmdRemote)

    #install kube proxy
    def installKbsProxy(self, nodename):
        node_env1 = self.getEnv("master1")
        # 初始化远程工具对象
        robj_master1 = Remote(node_env1)

        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        node_env = self.getEnv(nodename)
        # 初始化远程工具对象
        robj = Remote(node_env)

        remoteSslPath = self.getRemotePath('remoteSslPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')
        remoteSystemdPath = self.getRemotePath('remoteSystemdPath')
        tmpPath = self.getLocalPath('tmpPath')
        kbsBinPath = self.getLocalPath('kbsBinPath')
        kbsConfigPath = self.getLocalPath('kbsConfigPath')

        #download proxy cert files from master1
        robj_master1.download(remoteSslPath+"/kube-proxy.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/kube-proxy.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/kube-proxy-key.pem", tmpPath+"/")

        #download proxy kubeconfig files from admin node
        robj_admin.download(remoteCfgPath+"/kube-proxy.kubeconfig", tmpPath+"/")

        robj_master1.download(remoteSslPath+"/front-proxy-ca.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/front-proxy-ca-key.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/front-proxy-client.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/front-proxy-client.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/front-proxy-client-key.pem", tmpPath+"/")

        robj.upload(tmpPath+"/front-proxy-ca.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/front-proxy-ca-key.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/front-proxy-client.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/front-proxy-client.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/front-proxy-client-key.pem", remoteSslPath+"/")

        #stop relative service if the service is running
        cmdRemote = "systemctl stop kube-proxy"
        robj.sudo(cmdRemote)

        #install some packages for proxy
        cmdRemote = "yum install -y ipvsadm ipset conntrack"
        robj.sudo(cmdRemote)

        #upload binary file for kube processes
        if robj.checkpath(remoteBinPath+"/kube-proxy") == False:
            robj.upload(kbsBinPath+"/kube-proxy", remoteBinPath+"/")

        #upload proxy cert files to node1
        robj.upload(tmpPath+"/kube-proxy.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/kube-proxy-key.pem", remoteSslPath+"/")

        #upload proxy kubeconfig files to node1
        robj.upload(tmpPath+"/kube-proxy.kubeconfig", remoteCfgPath+"/")

        #upload systemd service files to node1
        robj.upload(kbsConfigPath+"/kube-proxy.service", remoteSystemdPath+"/")

        #upload proxy service config file
        sedRegex = "sed \"s/^--hostname-override={nodeName}/--hostname-override=%s/g\"" % node_env.host
        sedRegex = sedRegex + " | sed \"s/{podClusterIpRange}/%s/g\""% self.podClusterIpRange
        file_tmp = tmpPath + "/kube-proxy.conf"
        file_config = kbsConfigPath + "/kube-proxy.conf"
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj.local(cmd_local)
        # 上传文件到远程主机
        robj.upload(file_tmp, remoteCfgPath+"/", True)

        print("systemd daemon reload ...")
        cmdRemote = "systemctl daemon-reload"
        robj.sudo(cmdRemote)
        print("enable proxy service ...")
        cmdRemote = "systemctl enable kube-proxy.service"
        robj.sudo(cmdRemote)
        print("restart proxy service ...")
        cmdRemote = "systemctl restart kube-proxy.service"
        robj.sudo(cmdRemote)
        print("check proxy service ...")
        cmdRemote = "systemctl status kube-proxy.service"
        robj.sudo(cmdRemote)

    #install kubelet
    def installKbsKubelet(self, nodename):
        node_env = self.getEnv(nodename)
        # 初始化远程工具对象
        robj = Remote(node_env)

        print("node ip: "+node_env.host)

        node_env1 = self.getEnv("master1")
        # 初始化远程工具对象
        robj_master1 = Remote(node_env1)

        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        print("master ip: "+node_env1.host)

        remoteSslPath = self.getRemotePath('remoteSslPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')
        remoteSystemdPath = self.getRemotePath('remoteSystemdPath')
        tmpPath = self.getLocalPath('tmpPath')
        kbsBinPath = self.getLocalPath('kbsBinPath')
        kbsConfigPath = self.getLocalPath('kbsConfigPath')

        #download ca files from master1 to local
        robj_master1.download(remoteSslPath+"/ca.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca-key.pem", tmpPath+"/")
        #download etcd ca files from master1 to local
        robj_master1.download(remoteSslPath+"/etcd.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/etcd.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/etcd-key.pem", tmpPath+"/")
        
        robj_master1.download(remoteCfgPath+"/token.csv", tmpPath+"/")

        #download kubeconfig files from admin to local
        robj_admin.download(remoteCfgPath+"/bootstrap.kubeconfig", tmpPath+"/")

        #stop relative service if the service is running
        cmdRemote = "systemctl stop kube-kubelet"
        robj.sudo(cmdRemote)

        #upload binary file for kube processes
        if robj.checkpath(remoteBinPath+"/kubelet") == False:
            robj.upload(kbsBinPath+"/kubelet", remoteBinPath+"/")

        #upload ca files to node1
        robj.upload(tmpPath+"/ca.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/ca.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/ca-key.pem", remoteSslPath+"/")

        #upload etcd ca files to node1
        robj.upload(tmpPath+"/etcd.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/etcd.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/etcd-key.pem", remoteSslPath+"/")

        #upload config files to node1
        robj.upload(tmpPath+"/bootstrap.kubeconfig", remoteCfgPath+"/")
        robj.upload(tmpPath+"/token.csv", remoteCfgPath+"/")

        sedRegex = "sed \"s/{serviceClusterDnsIp}/%s/g\"" % self.serviceClusterDnsIp
        
        file_tmp = tmpPath + "/kubelet.config"
        file_config = kbsConfigPath + "/kubelet.config"
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj.local(cmd_local)

        # 上传文件到远程主机
        robj.upload(file_tmp, remoteCfgPath+"/")

        #upload systemd service files to node
        robj.upload(kbsConfigPath+"/kube-kubelet.service", remoteSystemdPath+"/")

        print("node ip: "+node_env.host)

        #upload kubelet service config file
        file_config = kbsConfigPath + "/kube-kubelet.conf"
        file_tmp = tmpPath + "/kube-kubelet.conf"
        sedRegex = "sed \"s/^--hostname-override={nodeName}/--hostname-override=%s/g\"" % node_env.host
        sedRegex = sedRegex + " | sed \"s/^--network-plugin={pluginName}//g\""
        sedRegex = sedRegex + " | sed \"s/^--cni-conf-dir={confDir}//g\""
        sedRegex = sedRegex + " | sed \"s/^--cni-bin-dir={binDir}//g\""
        sedRegex = sedRegex + " | sed \"s/{serviceClusterDnsIp}/%s/g\""% self.serviceClusterDnsIp
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj.local(cmd_local)
        # 上传文件到远程主机
        robj.upload(file_tmp, remoteCfgPath, True)

        print("systemd daemon reload ...")
        cmdRemote = "systemctl daemon-reload"
        robj.sudo(cmdRemote)

        print("enable kubelet service ...")
        cmdRemote = "systemctl enable kube-kubelet.service"
        robj.sudo(cmdRemote)

        print("restart kubelet service ...")
        cmdRemote = "systemctl restart kube-kubelet.service"
        robj.sudo(cmdRemote)

        print("check kubelet service ...")
        cmdRemote = "systemctl status kube-kubelet.service"
        robj.sudo(cmdRemote)
        
        print("sleep 5 seconds ...")
        cmdRemote = "sleep 5"
        robj.sudo(cmdRemote)

        print("restart kube apiserver ...")
        cmdRemote = "systemctl restart kube-apiserver"
        robj_master1.sudo(cmdRemote)

        print("show csr info: ")
        cmdRemote = remoteBinPath + "/kubectl get csr"
        robj_admin.sudo(cmdRemote)
        
        print("pass tls request: ")
        cmdRemote = remoteBinPath + "/kubectl get csr | grep 'Pending'"
        cmdRemote = cmdRemote + " | awk 'NR>0 {print $1}'"
        cmdRemote = cmdRemote + " | xargs "+remoteBinPath+"/kubectl certificate approve"
        robj_admin.sudo(cmdRemote)

    #validate
    def validKbsNode(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        # remoteDemoPath = self.getRemotePath('remoteDemoPath')
        # kbsConfigPath = self.getLocalPath('kbsConfigPath')

        print("show csr info: ")
        cmdRemote = remoteBinPath + "/kubectl get csr"
        robj_admin.sudo(cmdRemote)
        print("pass tls request: ")
        cmdRemote = remoteBinPath + "/kubectl get csr | grep 'Pending'"
        cmdRemote = cmdRemote + " | awk 'NR>0 {print $1}'"
        cmdRemote = cmdRemote + " | xargs "+remoteBinPath+"/kubectl certificate approve"
        robj_admin.sudo(cmdRemote)

        #delete old anonymous role binding in master1
        cmdRemote = remoteBinPath + "/kubectl delete clusterrolebinding/cluster-system-anonymous"
        robj_admin.sudo(cmdRemote)

        #create role binding in master1
        cmdRemote = remoteBinPath + "/kubectl create clusterrolebinding cluster-system-anonymous"
        cmdRemote = cmdRemote + " --clusterrole=cluster-admin"
        cmdRemote = cmdRemote + " --user=system:anonymous"
        robj_admin.sudo(cmdRemote)

        print("show cluster nodes info: ")
        cmdRemote = remoteBinPath + "/kubectl get node -o wide"
        robj_admin.sudo(cmdRemote)

        

