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

class Etcd(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #install etcd node normal
    def installEtcdNodeNormal(self, nodename):
        node_env = self.getEnv(nodename)
        # 初始化远程工具对象
        robj = Remote(node_env)

        remoteSslPath = self.getRemotePath('remoteSslPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')
        remoteSystemdPath = self.getRemotePath('remoteSystemdPath')
        remoteEtcdDataPath = self.getRemotePath('remoteEtcdDataPath')

        etcdBinPath = self.getLocalPath('etcdBinPath')
        etcdConfigPath = self.getLocalPath('etcdConfigPath')
        tmpPath = self.getLocalPath('tmpPath')

        #upload ca files
        robj.upload(tmpPath+"/ca.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/ca.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/ca-key.pem", remoteSslPath+"/")
        #upload etcd ca files
        robj.upload(tmpPath+"/etcd.csr", remoteSslPath+"/")
        robj.upload(tmpPath+"/etcd.pem", remoteSslPath+"/")
        robj.upload(tmpPath+"/etcd-key.pem", remoteSslPath+"/")

        #upload binary file for etcd processes
        if robj.checkpath((remoteBinPath+"/etcd")) == False:
            robj.upload(etcdBinPath+"/etcd", remoteBinPath+"/")

        if robj.checkpath((remoteBinPath+"/etcdctl")) == False:
            robj.upload(etcdBinPath+"/etcdctl", remoteBinPath+"/")

        #upload etcd config file
        file_config = etcdConfigPath + "/etcd.conf"
        file_tmp = tmpPath + "/etcd.conf"

        sedRegex = "sed \"s/{etcdNodeName}/%s/g\"" % ("etcd-"+nodename)
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp}/%s/g\"" % node_env.host

        sedRegex = sedRegex + " | sed \"s/{etcdNodeName1}/%s/g\"" % ("etcd-"+"master1")
        node1_env = self.getEnv("master1")
        etcdNodeIp1 = node1_env.host
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp1}/%s/g\"" % etcdNodeIp1

        sedRegex = sedRegex + " | sed \"s/{etcdNodeName2}/%s/g\"" % ("etcd-"+"master2")
        node2_env = self.getEnv("master2")
        etcdNodeIp2 = node2_env.host
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp2}/%s/g\"" % etcdNodeIp2

        sedRegex = sedRegex + " | sed \"s/{etcdNodeName3}/%s/g\"" % ("etcd-"+"master3")
        node3_env = self.getEnv("master3")
        etcdNodeIp3 = node3_env.host
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp3}/%s/g\"" % etcdNodeIp3

        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj.local(cmd_local)    
        
        robj.upload(file_tmp, remoteCfgPath+"/")
        robj.upload(etcdConfigPath+"/etcd.service", remoteSystemdPath+"/")

        if (remoteEtcdDataPath != "" and remoteEtcdDataPath != "/" and robj.checkpath(remoteEtcdDataPath)):
            robj.rmfile(remoteEtcdDataPath+"/*")
            print("cache files of etcd is removed ...")
            robj.sudo("ls -l "+remoteEtcdDataPath+"/")
        else:
            robj.mkdir(remoteEtcdDataPath)

        #systemd for etcd process
        robj.sudo("systemctl daemon-reload")
        robj.sudo("systemctl enable etcd.service")

        cmdRemote="nohup systemctl restart etcd.service &> /dev/null &"
        robj.sudo(cmdRemote)

    #install etcd node prepare
    def installEtcdNodePrepare(self):
        #stop relative service if the service is running
        print("stop relative service if the service is running ...")

        node_env1 = self.getEnv("master1")
        # 初始化远程工具对象
        robj_master1 = Remote(node_env1)
        print("stop etcd service in master1")
        robj_master1.sudo("systemctl stop etcd")
        node_env2 = self.getEnv("master2")
        # 初始化远程工具对象
        robj_master2 = Remote(node_env2)
        print("stop etcd service in master2")
        robj_master2.sudo("systemctl stop etcd")
        node_env3 = self.getEnv("master3")
        # 初始化远程工具对象
        robj_master3 = Remote(node_env3)
        print("stop etcd service in master3")
        robj_master3.sudo("systemctl stop etcd")

        remoteSslPath = self.getRemotePath('remoteSslPath')
        remoteLocalBinPath = self.getRemotePath('remoteLocalBinPath')
        etcdConfigPath = self.getLocalPath('etcdConfigPath')
        tmpPath = self.getLocalPath('tmpPath')

        #upload ca cert config file
        robj_master1.upload(etcdConfigPath+"/ca-csr.json", remoteSslPath+"/")
        robj_master1.upload(etcdConfigPath+"/ca-config.json", remoteSslPath+"/")
        #upload etcd csr file
        file_config = etcdConfigPath + "/etcd-csr.json"
        file_tmp = tmpPath + "/etcd-csr.json"

        node1_env = self.getEnv("master1")
        etcdNodeIp1 = node1_env.host
        sedRegex = "sed \"s/{etcdNodeIp1}/%s/g\"" % etcdNodeIp1

        node2_env = self.getEnv("master2")
        etcdNodeIp2 = node2_env.host
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp2}/%s/g\"" % etcdNodeIp2

        node3_env = self.getEnv("master3")
        etcdNodeIp3 = node3_env.host
        sedRegex = sedRegex + " | sed \"s/{etcdNodeIp3}/%s/g\"" % etcdNodeIp3
        
        node4_env = self.getEnv("node1")
        workerNodeIp = node4_env.host
        sedRegex = sedRegex + " | sed \"s/{workerNodeIp}/%s/g\"" % workerNodeIp
            
        cmd_local = "cat %s | %s > %s" % (file_config, sedRegex, file_tmp)
        robj_master1.local(cmd_local)    
        
        robj_master1.upload(file_tmp, remoteSslPath+"/")

        # generate ca root cert
        cmdRemote = remoteLocalBinPath+"/cfssl gencert -initca "+remoteSslPath+"/ca-csr.json"
        cmdRemote = cmdRemote + " | "+remoteLocalBinPath+"/cfssljson -bare "+remoteSslPath+"/ca"
        robj_master1.sudo(cmdRemote)

        #generate etcd cert for each node
        cmdRemote = remoteLocalBinPath+"/cfssl gencert -ca="+remoteSslPath+"/ca.pem"
        cmdRemote = cmdRemote + " -ca-key="+remoteSslPath+"/ca-key.pem"
        cmdRemote = cmdRemote + " -config="+remoteSslPath+"/ca-config.json"
        cmdRemote = cmdRemote + " -profile=kubernetes "+remoteSslPath+"/etcd-csr.json"
        cmdRemote = cmdRemote + " | "+remoteLocalBinPath+"/cfssljson -bare "+remoteSslPath+"/etcd"
        robj_master1.sudo(cmdRemote)

        #download ca files form master1 to local
        robj_master1.download(remoteSslPath+"/ca.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/ca-key.pem", tmpPath+"/")
        #download etcd ca files form master1 to local
        robj_master1.download(remoteSslPath+"/etcd.csr", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/etcd.pem", tmpPath+"/")
        robj_master1.download(remoteSslPath+"/etcd-key.pem", tmpPath+"/")

    #validate
    def validEtcd(self):
        node_env1 = self.getEnv("master1")
        # 初始化远程工具对象
        robj_master1 = Remote(node_env1)

        robj_master1.sudo("systemctl status etcd")

        node_env2 = self.getEnv("master2")
        # 初始化远程工具对象
        robj_master2 = Remote(node_env2)

        robj_master2.sudo("systemctl status etcd")

        node_env3 = self.getEnv("master3")
        # 初始化远程工具对象
        robj_master3 = Remote(node_env3)

        robj_master3.sudo("systemctl status etcd")

        remoteSslPath = self.getRemotePath('remoteSslPath')

        cmdValid0 = " /opt/kubernetes/bin/etcdctl"
        cmdValid1 = " --endpoints https://"+node_env1.host+":2379"
        cmdValid1 = cmdValid1 + ",https://"+node_env2.host+":2379,https://"+node_env3.host+":2379"
        cmdValid2_v2=" --ca-file="+remoteSslPath+"/ca.pem"
        cmdValid3_v2=" --cert-file="+remoteSslPath+"/etcd.pem"
        cmdValid4_v2=" --key-file="+remoteSslPath+"/etcd-key.pem"
        cmdValidVersion2="ETCDCTL_API=2 "+cmdValid0+" "+cmdValid1+" "+cmdValid2_v2
        cmdValidVersion2= cmdValidVersion2+" "+cmdValid3_v2+" "+cmdValid4_v2
        robj_master1.sudo(cmdValidVersion2+" cluster-health")
        robj_master1.sudo(cmdValidVersion2+" member list")
        robj_master1.sudo(cmdValidVersion2+" ls / -r")

