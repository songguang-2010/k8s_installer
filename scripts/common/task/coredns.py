#!/usr/bin/env python3
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本主要负责k8s集群安装前的相关准备工作

import copy
import os

# 导入自定义工具库
# lib_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(lib_path)
from lib.remote import Remote
from lib.xmlFile import XmlFile
from lib.base import Base

class Coredns(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #coredns validate
    def validCoredns(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        # remotePluginPath = self.getRemotePath('remotePluginPath')

        # corednsConfigPath = self.getLocalPath('corednsConfigPath')

        #show pod list
        print("show pod list in default ...")
        cmdRemote = remoteBinPath + "/kubectl get pods -o wide"
        robj_admin.sudo(cmdRemote)

        print("show service list in default ...")
        cmdRemote = remoteBinPath + "/kubectl get services -o wide"
        robj_admin.sudo(cmdRemote)

        #show pod list
        print("show pod list in kube-system ...")
        cmdRemote = remoteBinPath + "/kubectl get pods -n kube-system -o wide"
        robj_admin.sudo(cmdRemote)
        print("")

        #show service list
        print("show service list in kube-system ...")
        cmdRemote = remoteBinPath + "/kubectl get services -n kube-system -o wide"
        robj_admin.sudo(cmdRemote)

        #Verify that the search path and name server are set up
        print("check content in resolv.conf ...")
        cmdRemote = remoteBinPath + "/kubectl exec busybox cat /etc/resolv.conf"
        robj_admin.sudo(cmdRemote)

        #verify endpoints to expose
        cmdRemote = remoteBinPath + "/kubectl get endpoints"
        robj_admin.sudo(cmdRemote)

        #exec cmd in busybox container terminal, and test dns service
        print("test dns service in container busybox ...")
        cmdRemote = remoteBinPath + "/kubectl exec busybox -- nslookup kubernetes"
        robj_admin.sudo(cmdRemote)

    def installCoredns(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        tmpPath = self.getLocalPath('tmpPath')
        corednsConfigPath = self.getLocalPath('corednsConfigPath')

        #upload
        robj_admin.upload(corednsConfigPath+"/coredns-rbac.yaml", remotePluginPath+"/coredns/", True)
        robj_admin.upload(corednsConfigPath+"/coredns-sa.yaml", remotePluginPath+"/coredns/", True)
        robj_admin.upload(corednsConfigPath+"/coredns-configmap.yaml", remotePluginPath+"/coredns/", True)
        robj_admin.upload(corednsConfigPath+"/coredns-deployment.yaml", remotePluginPath+"/coredns/", True)

        ips_data = self.config_object.get_node_by_attr("name", "ips")
        serviceClusterDnsIp = ips_data.find('serviceClusterDnsIp').text

        sedRegex = "sed \"s/{serviceClusterDnsIp}/%s/g\"" % serviceClusterDnsIp
        
        file_tmp = tmpPath + "/coredns-service.yaml"
        file_config = corednsConfigPath + "/coredns-service.yaml"
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj_admin.local(cmd_local)

        # 上传文件到远程主机
        robj_admin.upload(file_tmp, remotePluginPath+"/coredns/", True)

        #install
        cmdRemote = remoteBinPath + "/kubectl create -f "+remotePluginPath+"/coredns/coredns-rbac.yaml"
        robj_admin.sudo(cmdRemote)
        cmdRemote = remoteBinPath + "/kubectl create -f "+remotePluginPath+"/coredns/coredns-sa.yaml"
        robj_admin.sudo(cmdRemote)
        cmdRemote = remoteBinPath + "/kubectl create -f "+remotePluginPath+"/coredns/coredns-configmap.yaml"
        robj_admin.sudo(cmdRemote)
        cmdRemote = remoteBinPath + "/kubectl create -f "+remotePluginPath+"/coredns/coredns-deployment.yaml"
        robj_admin.sudo(cmdRemote)
        cmdRemote = remoteBinPath + "/kubectl create -f "+remotePluginPath+"/coredns/coredns-service.yaml"
        robj_admin.sudo(cmdRemote)

    def deleteCoredns(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        # tmpPath = self.getLocalPath('tmpPath')
        # corednsConfigPath = self.getLocalPath('corednsConfigPath')

        #delete coredns resources 
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/coredns/coredns-configmap.yaml"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/coredns/coredns-deployment.yaml"
        robj_admin.sudo(cmdRemote)
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/coredns/coredns-rbac.yaml"
        robj_admin.sudo(cmdRemote)
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/coredns/coredns-sa.yaml"
        robj_admin.sudo(cmdRemote)
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/coredns/coredns-service.yaml"
        robj_admin.sudo(cmdRemote)


