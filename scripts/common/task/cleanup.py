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

class Cleanup(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #cleanup
    def cleanup(self, nodename):
        node_env = self.getEnv(nodename)
        # 初始化远程工具对象
        robj_node = Remote(node_env)

        remoteEtcdDataPath = self.getRemotePath('remoteEtcdDataPath')
        remoteSslPath = self.getRemotePath('remoteSslPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')

        tmpPath = self.getLocalPath('tmpPath')

        cmdRemote = "systemctl stop kube-kubelet"
        robj_node.sudo(cmdRemote)
        cmdRemote = "systemctl stop kube-proxy"
        robj_node.sudo(cmdRemote)
        cmdRemote = "systemctl stop kube-apiserver"
        robj_node.sudo(cmdRemote)
        cmdRemote = "systemctl stop kube-controller-manager"
        robj_node.sudo(cmdRemote)
        cmdRemote = "systemctl stop kube-scheduler"
        robj_node.sudo(cmdRemote)
        cmdRemote = "systemctl stop docker"
        robj_node.sudo(cmdRemote)

        robj_node.cleanup(remoteEtcdDataPath)
        print("cache files of etcd is removed ...")
        robj_node.sudo("ls -l "+remoteEtcdDataPath+"/")
            
        res = robj_node.cleanup(remoteSslPath)
        if(res == False):
            print("failed to cleanup "+remoteSslPath)
        print("ssl files is removed ...")
        robj_node.sudo("ls -l "+remoteSslPath+"/")

        robj_node.cleanup(remoteCfgPath)
        print("config files is removed ...")
        robj_node.sudo("ls -l "+remoteCfgPath+"/")

        robj_node.cleanupLocal(tmpPath, True)
        print("tmp files is removed ...")
        robj_node.local("ls -l "+tmpPath+"/")

