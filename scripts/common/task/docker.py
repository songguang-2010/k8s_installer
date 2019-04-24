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

class Docker(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #install docker private repository
    def installDockerPrivate(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        docker_data = self.config_object.get_node_by_attr("name", "docker")
        dockerUsername = docker_data.find('username').text
        dockerPassword = docker_data.find('password').text
        dockerDomain = docker_data.find('domain').text

        tmpPath = self.getLocalPath('tmpPath')
        dockerConfigPath = self.getLocalPath('dockerConfigPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        #login docker registry
        cmdRemote = "docker login --username=%s --password=%s %s" % (dockerUsername, dockerPassword, dockerDomain)
        robj_admin.sudo(cmdRemote)

        #download docker login config file form master1 to local
        robj_admin.download("/root/.docker/config.json", tmpPath+"/")

        #view docker login config file content in local, and generate login credentials
        # dockerSecret = $(cat ./config.json | base64 -w 0)
        file_config = dockerConfigPath+"/registry-pull-secret.yaml"
        file_tmp = tmpPath+"/registry-pull-secret.yaml"
        with open(tmpPath+'/config.json') as file_object:
            contents = file_object.read()
            dockerSecret = base64.b64encode(contents.rstrip().encode("utf-8")).decode("utf-8")
            print("dockerSecret: "+dockerSecret)
            sedRegex = "s/{dockerSecret}/%s/g" % dockerSecret.replace("/", r"\/")
            cmdLocal = "cat %s | sed \"%s\" > %s" % (file_config, sedRegex, file_tmp)
            print(cmdLocal)
            robj_admin.local(cmdLocal)
            robj_admin.upload(file_tmp, remoteCfgPath+"/", True)

        #create docker secret pod
        cmdRemote = remoteBinPath + "/kubectl create -f "+remoteCfgPath+"/registry-pull-secret.yaml"
        robj_admin.sudo(cmdRemote)

        #get docker secret
        cmdRemote = remoteBinPath + "/kubectl get secret"
        robj_admin.sudo(cmdRemote)

    #delete docker private
    def deleteDockerPrivate(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remoteCfgPath = self.getRemotePath('remoteCfgPath')

        cmdRemote = remoteBinPath + "/kubectl delete -f "+remoteCfgPath+"/registry-pull-secret.yaml"
        robj_admin.sudo(cmdRemote)
