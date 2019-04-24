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

class Cni(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #install
    def installCniNodeNormal(self, nodename):
        node_env = self.getEnv(nodename)
        # 初始化远程工具对象
        robj_node = Remote(node_env)

        cniBinPath = self.getLocalPath('cniBinPath')
        cniConfigPath = self.getLocalPath('cniConfigPath')
        kbsConfigPath = self.getLocalPath('kbsConfigPath')
        tmpPath = self.getLocalPath('tmpPath')
        remoteCniBinPath = self.getRemotePath('remoteCniBinPath')
        remoteCniCfgPath = self.getRemotePath('remoteCniCfgPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')

        #stop relative service if the service is running
        cmdRemote = "systemctl stop kube-kubelet"
        robj_node.sudo(cmdRemote)

        # upload cni files
        robj_node.upload(cniBinPath+"/loopback", remoteCniBinPath+"/")
        robj_node.upload(cniBinPath+"/portmap", remoteCniBinPath+"/")
        robj_node.upload(cniConfigPath+"/99-loopback.conf", remoteCniCfgPath+"/")

        #upload kubelet service config file for cni
        file_config = kbsConfigPath + "/kube-kubelet.conf"
        file_tmp = tmpPath + "/kube-kubelet.conf"
        plugin_name = "cni"
        sedRegex = "sed \"s/^--hostname-override={nodeName}/--hostname-override=%s/g\"" % node_env.host
        sedRegex = sedRegex + " | sed \"s/^--network-plugin={pluginName}/--network-plugin=%s/g\"" % plugin_name
        sedRegex = sedRegex + " | sed \"s/^--cni-conf-dir={confDir}/--cni-conf-dir=%s/g\"" % remoteCniCfgPath.replace("/", "\/")
        sedRegex = sedRegex + " | sed \"s/^--cni-bin-dir={binDir}/--cni-bin-dir=%s/g\"" % remoteCniBinPath.replace("/", "\/")
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        print(cmd_local)
        robj_node.local(cmd_local)
        # 上传文件到远程主机
        robj_node.upload(file_tmp, remoteCfgPath+"/", True)

        print("systemd daemon reload ...")
        cmdRemote = "systemctl daemon-reload"
        robj_node.sudo(cmdRemote)

        print("restart kubelet service ...")
        cmdRemote = "systemctl restart kube-kubelet.service"
        robj_node.sudo(cmdRemote)

        print("check kubelet service ...")
        cmdRemote = "systemctl status kube-kubelet.service"
        robj_node.sudo(cmdRemote)

    #validate
    def validCniNodeNormal(self, nodename):
        node_env = self.getEnv(nodename)
        # 初始化远程工具对象
        robj_node = Remote(node_env)

        print("check kubelet service ...")
        cmdRemote = "systemctl status kube-kubelet.service"
        robj_node.sudo(cmdRemote)

