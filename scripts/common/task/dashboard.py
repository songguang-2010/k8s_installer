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

class Dashboard(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #dashboard validate
    def validDashboard(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')

        #list pod and service 
        cmdRemote = remoteBinPath + "/kubectl get pod,svc -n kube-system -o wide"
        robj_admin.sudo(cmdRemote)

        #cluster info
        cmdRemote = remoteBinPath + "/kubectl cluster-info -n kube-system"
        robj_admin.sudo(cmdRemote)

        #list tokens of kube-system namespaces
        cmdRemote = remoteBinPath + "/kubectl -n kube-system get secret"
        robj_admin.sudo(cmdRemote)

        #get token name to login
        cmdRemote = remoteBinPath + "/kubectl -n kube-system get secret"
        cmdRemote = cmdRemote + " | grep kubernetes-dashboard-token | awk '{print $1}'"
        robj_admin.sudo(cmdRemote)
        secretName = robj_admin.getResult().stdout.rstrip()
        # print(secretName)

        cmdRemote = remoteBinPath + "/kubectl -n kube-system describe secret "+secretName
        robj_admin.sudo(cmdRemote)

    def installDashboard(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        dashboardConfigPath = self.getLocalPath('dashboardConfigPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')

        #label admin node for install dashboard
        cmdRemote = remoteBinPath + "/kubectl label node "+admin_env.host+" role=admin"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl delete -f "
        cmdRemote = cmdRemote + remotePluginPath + "/dashboard/kubernetes-dashboard.yaml"
        robj_admin.sudo(cmdRemote)

        robj_admin.upload(dashboardConfigPath+"/kubernetes-dashboard.yaml", remotePluginPath+"/dashboard/")
        
        cmdRemote = remoteBinPath + "/kubectl apply -f "
        cmdRemote = cmdRemote + remotePluginPath + "/dashboard/kubernetes-dashboard.yaml"
        robj_admin.sudo(cmdRemote)

    def deleteDashboard(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')

        cmdRemote = remoteBinPath + "/kubectl delete -f "
        cmdRemote = cmdRemote + remotePluginPath+"/dashboard/kubernetes-dashboard.yaml"
        robj_admin.sudo(cmdRemote)

        
