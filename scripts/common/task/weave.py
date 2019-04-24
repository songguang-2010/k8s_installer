#!/usr/bin/env python3
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本主要负责k8s集群安装前的相关准备工作

import copy
import os
import base64

# 导入自定义工具库
# lib_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(lib_path)
from lib.remote import Remote
from lib.xmlFile import XmlFile
from lib.base import Base

class Weave(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #install
    def installWeaveNodeNormal(self, nodename):
        node_env = self.getEnv(nodename)
        # 初始化远程工具对象
        robj_node = Remote(node_env)

        #install bridge tools
        cmdRemote = "yum install -y bridge-utils"
        robj_node.sudo(cmdRemote)

    #after install
    def installWeaveNodeAfter(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        weaveConfigPath = self.getLocalPath('weaveConfigPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        tmpPath = self.getLocalPath('tmpPath')

        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/weave/weave.yaml"
        robj_admin.sudo(cmdRemote)

        #upload yaml file 
        ips_data = self.config_object.get_node_by_attr("name", "ips")
        podClusterIpRange = ips_data.find('podClusterIpRange').text.replace("/", "\/")

        sedRegex = "sed \"s/{podClusterIpRange}/%s/g\"" % podClusterIpRange
        
        file_tmp = tmpPath + "/weave.yaml"
        file_config = weaveConfigPath + "/weave.yaml"
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj_admin.local(cmd_local)

        # 上传文件到远程主机
        robj_admin.upload(file_tmp, remotePluginPath+"/weave/", True)

        #install weave plugin
        # yamlWeave="https://cloud.weave.works/k8s/net?k8s-version=\$(${remoteBinPath}/kubectl version | base64 | tr -d '\\\n')"
        cmdRemote = remoteBinPath + "/kubectl apply -f "+remotePluginPath+"/weave/weave.yaml"
        robj_admin.sudo(cmdRemote)

    #validate
    def validWeaveNodeAll(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')

        # 在远端主机执行命令
        print("list weave net pods: ")
        cmdRemote = remoteBinPath + "/kubectl get pods,services -n kube-system -l name=weave-net -o wide"
        robj_admin.sudo(cmdRemote)
        
        cmdRemote = remoteBinPath + "/kubectl get pods -n kube-system -l name=weave-net"
        cmdRemote = cmdRemote + " | awk 'NR==2 {print $1}'"
        robj_admin.sudo(cmdRemote)
        # kubectl exec -n kube-system {podname} -c weave -- /home/weave/weave --local status
        cmdRemote = remoteBinPath + "/kubectl exec -c weave -n kube-system $(%s)" % cmdRemote
        cmdRemote = cmdRemote + " -- /home/weave/weave --local status"
        print(cmdRemote)
        robj_admin.sudo(cmdRemote)

    def deleteWeave(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')

        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/weave/weave.yaml"
        robj_admin.sudo(cmdRemote)

