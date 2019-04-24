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

class Ingress(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #ingress validate
    def validIngress(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        # remotePluginPath = self.getRemotePath('remotePluginPath')

        # corednsConfigPath = self.getLocalPath('corednsConfigPath')

        #get namespaces
        cmdRemote = remoteBinPath + "/kubectl get ns"
        robj_admin.sudo(cmdRemote)

        #get pod list in namespace ingress-nginx
        cmdRemote = remoteBinPath + "/kubectl get rs,pods,svc -n ingress-nginx -o wide"
        robj_admin.sudo(cmdRemote)

        #get pod list in namespace default
        cmdRemote = remoteBinPath + "/kubectl get rs,pods,svc -n default -o wide"
        robj_admin.sudo(cmdRemote)

        #get process list listenning on 80 and 443 on target node
        # cmdRemote = "netstat -tnlp | egrep \"80|443\""

        #test myapp service cluterip in deploy node
        #curl {clusterIp}

        #get ingress
        cmdRemote = remoteBinPath + "/kubectl get ingress"
        robj_admin.sudo(cmdRemote)    

    def installIngress(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        # tmpPath = self.getLocalPath('tmpPath')
        ingressConfigPath = self.getLocalPath('ingressConfigPath')

        #remove
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/ingress/mandatory.yaml"
        robj_admin.sudo(cmdRemote)

        #upload yaml file
        robj_admin.upload(ingressConfigPath+"/mandatory.yaml", remotePluginPath+"/ingress/", True)

        #install
        cmdRemote = remoteBinPath + "/kubectl apply -f "+remotePluginPath+"/ingress/mandatory.yaml"
        robj_admin.sudo(cmdRemote)

    def deleteIngress(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        #delete ingress
        print("delete ingress ...")
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/ingress/mandatory.yaml"
        robj_admin.sudo(cmdRemote)
