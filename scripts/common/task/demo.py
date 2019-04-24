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

class Demo(Base):
    def __init__(self, config_object):
        Base.__init__(self, config_object)

    def __del__(self):
        pass

    #install nginx demo
    def installNginx(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')

        #uninstall old nginx pod and service
        # cmdRemote = remoteBinPath + "/kubectl delete -f "+remoteDemoPath+"/nginx-demo-deployment.yaml"
        # robj_master1.sudo(cmdRemote)

        #upload nginx-demo-deployment.yaml to master
        # robj_master1.upload(kbsConfigPath+"/nginx-demo-deployment.yaml", remoteDemoPath+"/")

        # create pod
        # cmdRemote = remoteBinPath + "/kubectl apply -f "+remoteDemoPath+"/nginx-demo-deployment.yaml"
        # robj_master1.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl run nginx --image=nginx --replicas=3"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl expose deployment nginx --port=88 --target-port=80 --type=NodePort"
        robj_admin.sudo(cmdRemote)

        # list pod and service
        cmdRemote = remoteBinPath + "/kubectl get pod,svc -o wide"
        robj_admin.sudo(cmdRemote)

    def deleteNginx(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')

        cmdRemote = remoteBinPath + "/kubectl delete deployment nginx"
        robj_admin.sudo(cmdRemote)

        cmdRemote = remoteBinPath + "/kubectl delete service nginx"
        robj_admin.sudo(cmdRemote)

    def installDemoBusybox(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        # tmpPath = self.getLocalPath('tmpPath')
        corednsConfigPath = self.getLocalPath('corednsConfigPath')

        #uninstall old service
        print("remove busybox container ...")
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/coredns/busybox.yaml"
        robj_admin.sudo(cmdRemote)

        #upload
        print("upload busybox yaml ...")
        robj_admin.upload(corednsConfigPath+"/busybox.yaml", remotePluginPath+"/coredns/")

        #install
        print("create busybox container ...")
        cmdRemote = remoteBinPath + "/kubectl create -f "+remotePluginPath+"/coredns/busybox.yaml"
        robj_admin.sudo(cmdRemote)

        print("sleep 5 seconds ...")
        robj_admin.sudo("sleep 5s")

        #view
        print("list pods of busybox ...")
        cmdRemote = remoteBinPath + "/kubectl get pods -o wide"
        robj_admin.sudo(cmdRemote)

    def deleteDemoBusybox(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')

        # tmpPath = self.getLocalPath('tmpPath')
        # corednsConfigPath = self.getLocalPath('corednsConfigPath')

        #uninstall old service
        print("remove busybox container ...")
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/coredns/busybox.yaml"
        robj_admin.sudo(cmdRemote)

        print("sleep 5 seconds ...")
        robj_admin.sudo("sleep 5s")

        #view
        print("list pods of busybox ...")
        cmdRemote = remoteBinPath + "/kubectl get pods -o wide"
        robj_admin.sudo(cmdRemote)

    def installDemoIngress(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')

        ingressConfigPath = self.getLocalPath('ingressConfigPath')

        #upload ingress backend
        robj_admin.upload(ingressConfigPath+"/nginx-ingress-backend.yaml", remotePluginPath+"/ingress/", True)

        #install ingress backend
        cmdRemote = remoteBinPath + "/kubectl apply -f "+remotePluginPath+"/ingress/nginx-ingress-backend.yaml"
        robj_admin.sudo(cmdRemote)

        #upload ingress rules
        robj_admin.upload(ingressConfigPath+"/nginx-ingress-rules.yaml", remotePluginPath+"/ingress/", True)

        #install ingress rules
        cmdRemote = remoteBinPath + "/kubectl apply -f "+remotePluginPath+"/ingress/nginx-ingress-rules.yaml"
        robj_admin.sudo(cmdRemote)

    def deleteDemoIngress(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')

        # ingressConfigPath = self.getLocalPath('ingressConfigPath')

        # remove ingress rules
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/ingress/nginx-ingress-rules.yaml"
        robj_admin.sudo(cmdRemote)

        # remove ingress backend
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/ingress/nginx-ingress-backend.yaml"
        robj_admin.sudo(cmdRemote)

    def installDemoIngressHttps(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')
        remoteSslPath = self.getRemotePath('remoteSslPath')

        ingressConfigPath = self.getLocalPath('ingressConfigPath')

        # tls support
        domainName = "sslexample.foo.com"
        secretName = domainName.replace(".", "-")

        print("generate tls key file ...")
        keyFile = remoteSslPath + "/tls-ingress-"+secretName+".key"
        certFile = remoteSslPath + "/tls-ingress-"+secretName+".crt"
        #generate tls key
        cmdRemote = "openssl genrsa -out "+keyFile+" 2048"
        robj_admin.sudo(cmdRemote)

        #generate tls cert
        print("generate tls cert file ...")
        cmdRemote = "openssl req -new -x509 -key "+keyFile+" -out "+certFile
        cmdRemote = cmdRemote + " -subj /C=CN/ST=Beijing/L=Beijing/O=DevOps/CN="+domainName
        robj_admin.sudo(cmdRemote)

        #generate secret
        print("generate secret ...")
        cmdRemote = remoteBinPath + "/kubectl create secret tls "+secretName
        cmdRemote = cmdRemote + " --cert="+certFile+" --key="+keyFile
        robj_admin.sudo(cmdRemote)

        #get secret
        print("get secret ...")
        cmdRemote = remoteBinPath + "/kubectl get secret"
        robj_admin.sudo(cmdRemote)

        #describe secret
        print("describe secret ...")
        cmdRemote = remoteBinPath + "/kubectl describe secret "+secretName
        robj_admin.sudo(cmdRemote)

        # remove ingress rules of https
        print("remove ingress rules of https ...")
        cmdRemote = remoteBinPath + "/kubectl delete -f "
        cmdRemote = cmdRemote + remotePluginPath + "/ingress/nginx-ingress-rules-https.yaml"
        robj_admin.sudo(cmdRemote)

        #upload ingress rules of https
        print("upload ingress rules yaml ...")
        robj_admin.upload(ingressConfigPath+"/nginx-ingress-rules-https.yaml", remotePluginPath+"/ingress/")
        
        #install ingress rules of https
        print("install ingress rules ...")
        cmdRemote = remoteBinPath + "/kubectl apply -f "
        cmdRemote = cmdRemote + remotePluginPath+"/ingress/nginx-ingress-rules-https.yaml"
        robj_admin.sudo(cmdRemote)
        
    def deleteDemoIngressHttps(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')
        # remoteSslPath = self.getRemotePath('remoteSslPath')

        #delete ingress rules of https
        print("delete ingress rules of https ...")
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/ingress/nginx-ingress-rules-https.yaml"
        robj_admin.sudo(cmdRemote)

    def validDemoIngressHttps(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        # remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')
        # remoteSslPath = self.getRemotePath('remoteSslPath')

        # ingressConfigPath = self.getLocalPath('ingressConfigPath')

        #get ingress
        cmdRemote = remoteBinPath + "/kubectl get ingress"
        robj_admin.sudo(cmdRemote)

        #describe ingress
        cmdRemote = remoteBinPath + "/kubectl describe ingress tls-example-ingress"
        robj_admin.sudo(cmdRemote)

    def validDemoIngress(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        # remotePluginPath = self.getRemotePath('remotePluginPath')
        remoteBinPath = self.getRemotePath('remoteBinPath')
        # remoteSslPath = self.getRemotePath('remoteSslPath')

        # ingressConfigPath = self.getLocalPath('ingressConfigPath')

        #get ingress
        cmdRemote = remoteBinPath + "/kubectl get ingress"
        robj_admin.sudo(cmdRemote)

        #describe inress
        cmdRemote = remoteBinPath + "/kubectl describe ingress simple-fanout-example"
        robj_admin.sudo(cmdRemote) 

        #test domain by curl after set hosts to parse domain name to ip
        #curl {domainName}  

    def installDemoDockerPrivate(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        docker_data = self.config_object.get_node_by_attr("name", "docker")
        dockerUsername = docker_data.find('username').text
        dockerPassword = docker_data.find('password').text
        dockerDomain = docker_data.find('domain').text

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')
        dockerConfigPath = self.getLocalPath('dockerConfigPath')

        #get docker secret
        cmdRemote = remoteBinPath + "/kubectl get secret"
        robj_admin.sudo(cmdRemote)

        #valid
        busyboxAddress = "registry.cn-beijing.aliyuncs.com/ducafe/busybox"
        cmdLocal = "docker images | grep %s | awk '{print $3}'" % busyboxAddress
        robj_admin.local(cmdLocal)
        imageId = robj_admin.getResult().stdout.rstrip()
        # print(robj_admin.getResult().exited)

        if imageId == "":
            print("upload busybox image to aliyun repository ...")
            cmdLocal = "docker pull registry.cn-beijing.aliyuncs.com/ducafe/busybox:1.24"
            robj_admin.local(cmdLocal)
            cmdLocal = "docker images | grep %s | awk '{print $3}'" % busyboxAddress
            robj_admin.local(cmdLocal)
            imageId = robj_admin.getResult().stdout.rstrip()
            #login docker registry
            cmdLocal = "docker login --username=%s --password=%s %s" % (dockerUsername, dockerPassword, dockerDomain)
            robj_admin.local(cmdLocal)
            cmdLocal = "docker tag %s %s/kube-systems/busybox-demo:1.24" % (imageId, dockerDomain)
            robj_admin.local(cmdLocal)
            cmdLocal = "docker images"
            robj_admin.local(cmdLocal)
            cmdLocal = "docker push %s/kube-systems/busybox-demo:1.24" % dockerDomain
            robj_admin.local(cmdLocal)

        #upload
        robj_admin.upload(dockerConfigPath+"/busybox-demo.yaml", remotePluginPath+"/docker/")

        #install
        cmdRemote = remoteBinPath + "/kubectl create -f "+remotePluginPath+"/docker/busybox-demo.yaml"
        robj_admin.sudo(cmdRemote)

        cmdRemote = "sleep 2s"
        robj_admin.sudo(cmdRemote)

    def deleteDemoDockerPrivate(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        # docker_data = self.config_object.get_node_by_attr("name", "docker")
        # dockerUsername = docker_data.find('username').text
        # dockerPassword = docker_data.find('password').text
        # dockerDomain = docker_data.find('domain').text

        remoteBinPath = self.getRemotePath('remoteBinPath')
        remotePluginPath = self.getRemotePath('remotePluginPath')
        # dockerConfigPath = self.getLocalPath('dockerConfigPath')

        #uninstall old service
        cmdRemote = remoteBinPath + "/kubectl delete -f "+remotePluginPath+"/docker/busybox-demo.yaml"
        print(cmdRemote)
        robj_admin.sudo(cmdRemote)

    def validDemoDockerPrivate(self):
        admin_env = self.getEnv("admin")
        # 初始化远程工具对象
        robj_admin = Remote(admin_env)

        remoteBinPath = self.getRemotePath('remoteBinPath')

        #view
        cmdRemote = remoteBinPath + "/kubectl get pods busybox-demo -o wide"
        robj_admin.sudo(cmdRemote)


