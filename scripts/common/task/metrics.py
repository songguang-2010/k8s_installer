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

class Metrics(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #metrics validate
    def validMetricsServer(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')

        #list pod and service 
        cmdRemote = remoteBinPath + "/kubectl get pods -l k8s-app=metrics-server -n kube-system -o wide"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath+"/kubectl get apiservice v1beta1.metrics.k8s.io -o yaml "
        robj_admin.sudo(cmdRemote)

        # cmdRemote = "yum install -y jq"
        # robj_admin.sudo(cmdRemote)

        # cmdRemote = " kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes" | jq"

    def installMetricsServer(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        metricsConfigPath = self.getLocalPath('metricsConfigPath')
        # kbsPluginPath = self.getLocalPath('kbsPluginPath')
        # tmpPath = self.getLocalPath('tmpPath')

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')

        # metricsConfigPath = kbsPluginPath + "/metrics-server"

        robj_admin.upload(metricsConfigPath+"/aggregated-metrics-reader.yaml", remotePluginPath+"/metrics/", True)
        robj_admin.upload(metricsConfigPath+"/auth-delegator.yaml", remotePluginPath+"/metrics/", True)
        robj_admin.upload(metricsConfigPath+"/auth-reader.yaml", remotePluginPath+"/metrics/", True)
        robj_admin.upload(metricsConfigPath+"/metrics-apiservice.yaml", remotePluginPath+"/metrics/", True)
        robj_admin.upload(metricsConfigPath+"/metrics-server-deployment.yaml", remotePluginPath+"/metrics/", True)
        robj_admin.upload(metricsConfigPath+"/metrics-server-service.yaml", remotePluginPath+"/metrics/", True)
        robj_admin.upload(metricsConfigPath+"/resource-reader.yaml", remotePluginPath+"/metrics/", True)
        robj_admin.upload(metricsConfigPath+"/metrics-server-ingress.yaml", remotePluginPath+"/metrics/", True)

        # robj_admin.upload(metricsConfigPath+"/auth-delegator.yaml", remotePluginPath+"/metrics/", True)
        # robj_admin.upload(metricsConfigPath+"/auth-reader.yaml", remotePluginPath+"/metrics/", True)
        # robj_admin.upload(metricsConfigPath+"/metrics-apiservice.yaml", remotePluginPath+"/metrics/", True)
        # robj_admin.upload(metricsConfigPath+"/metrics-server-service.yaml", remotePluginPath+"/metrics/", True)
        # robj_admin.upload(metricsConfigPath+"/resource-reader.yaml", remotePluginPath+"/metrics/", True)

        # file_config = metricsConfigPath + "/metrics-server-deployment.yaml"
        # file_tmp = tmpPath + "/metrics-server-deployment.yaml"
        # s1 = "k8s.gcr.io/metrics-server-amd64:v0.3.1".replace("/", "\/")
        # r1 = "registry.cn-beijing.aliyuncs.com/kube-systems/metrics-server:0.3.1".replace("/", "\/")
        # s2 = "k8s.gcr.io/addon-resizer:1.8.4".replace("/", "\/")
        # r2 = "registry.cn-beijing.aliyuncs.com/kube-systems/addon-resizer:1.8.4".replace("/", "\/")
        # sedRegex = "sed \"s/"+s1+"/"+r1+"/g\""
        # sedRegex = sedRegex + " | sed \"s/"+s2+"/"+r2+"/g\""
        # cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        # robj_admin.local(cmd_local)
        # # 上传文件到远程主机
        # robj_admin.upload(file_tmp, remotePluginPath+"/metrics/", True)
        
        cmdRemote = remoteBinPath + "/kubectl create -f "
        cmdRemote = cmdRemote + remotePluginPath + "/metrics/"
        robj_admin.sudo(cmdRemote)

    def deleteMetricsServer(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')

        cmdRemote = remoteBinPath + "/kubectl delete -f "
        cmdRemote = cmdRemote + remotePluginPath+"/metrics/"
        robj_admin.sudo(cmdRemote)

        
