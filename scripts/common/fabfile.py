#!/usr/bin/env python3
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本使用fabric api, 在本地操作远端主机资源
# 该脚本主要负责以下功能：
#
# 1.在远端主机上以sudo权限执行指定的命令

import os.path
import sys
import datetime
# import copy
# import csv
# import base64
from fabric import task
# from fabric import Connection
from invocations.console import confirm
# 导入自定义工具库
# lib_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(lib_path)
from lib.remote import Remote
from lib.xmlFile import XmlFile
from task.prepare import Prepare
from task.dashboard import Dashboard
from task.docker import Docker
from task.weave import Weave
from task.cni import Cni
from task.cleanup import Cleanup
from task.kbs import Kbs
from task.etcd import Etcd
from task.coredns import Coredns
from task.ingress import Ingress
from task.demo import Demo
from task.metrics import Metrics

# 获得当前文件所在目录
file_path = os.path.dirname(os.path.realpath(__file__))
# 获得应用根目录
app_path = os.path.dirname(os.path.dirname(file_path))

# 配置文件
config_file = app_path+"/config/config.xml"
config_object = XmlFile(config_file)

@task
def deleteMetricsServer(c):
    metrics = Metrics(config_object)
    metrics.deleteMetricsServer()

@task
def validMetricsServer(c):
    metrics = Metrics(config_object)
    metrics.validMetricsServer()
    
@task
def installMetricsServer(c):
    metrics = Metrics(config_object)
    metrics.installMetricsServer()

@task
def deleteDashboard(c):
    dashboard = Dashboard(config_object)
    dashboard.deleteDashboard()

@task
def validDashboard(c):
    dashboard = Dashboard(config_object)
    dashboard.validDashboard()
    
@task
def installDashboard(c):
    dashboard = Dashboard(config_object)
    dashboard.installDashboard()

@task
def validDemoDockerPrivate(c):
    demo = Demo(config_object)
    demo.validDemoDockerPrivate()

@task
def deleteDockerPrivate(c):
    docker = Docker(config_object)
    docker.deleteDockerPrivate()

@task
def installDockerPrivate(c):
    docker = Docker(config_object)
    docker.installDockerPrivate()

@task
def installDemoDockerPrivate(c):
    demo = Demo(config_object)
    demo.installDemoDockerPrivate()

@task
def deleteDemoDockerPrivate(c):
    demo = Demo(config_object)
    demo.deleteDemoDockerPrivate()

@task
def deleteWeave(c):
    weave = Weave(config_object)
    weave.deleteWeave()

@task
def validWeaveNodeAll(c):
    weave = Weave(config_object)
    weave.validWeaveNodeAll()

@task
def installWeaveNodeAfter(c):
    weave = Weave(config_object)
    weave.installWeaveNodeAfter()

@task
def installWeaveNodeNormal(c, nodename):
    weave = Weave(config_object)
    weave.installWeaveNodeNormal(nodename)

@task
def validCniNodeNormal(c, nodename):
    cni = Cni(config_object)
    cni.validCniNodeNormal(nodename)

@task
def installCniNodeNormal(c, nodename):
    cni = Cni(config_object)
    cni.installCniNodeNormal(nodename)

@task 
def cleanupComponents(c):
    demo = Demo(config_object)

    demo.deleteDemoIngressHttps()
    demo.deleteDemoIngress()

    ingress = Ingress(config_object)
    ingress.deleteIngress()

    dashboard = Dashboard(config_object)
    dashboard.deleteDashboard()
    
    demo.deleteNginx()

    demo.deleteDemoBusybox()

    coredns = Coredns(config_object)
    coredns.deleteCoredns()

    demo.deleteDemoDockerPrivate()

    weave = Weave(config_object)
    weave.deleteWeave()

@task 
def cleanupFiles(c, nodename):
    cleanup = Cleanup(config_object)
    cleanup.cleanup(nodename)

@task
def validKbsNode(c):
    kbs = Kbs(config_object)
    kbs.validKbsNode()

def installKbsKubelet(nodename):
    kbs = Kbs(config_object)
    kbs.installKbsKubelet(nodename)

def installKbsProxy(nodename):
    kbs = Kbs(config_object)
    kbs.installKbsProxy(nodename)

@task
def installKbsNodeNormal(c, nodename):
    installKbsKubelet(nodename)
    installKbsProxy(nodename)

@task 
def installKbsNodeBefore(c):
    kbs = Kbs(config_object)
    kbs.installKbsNodeBefore()

@task
def validKbsMaster(c):
    kbs = Kbs(config_object)
    kbs.validKbsMaster()

@task 
def installKbsMasterNormal(c, nodename):
    kbs = Kbs(config_object)
    kbs.installKbsMasterNormal(nodename)

@task
def installKbsMasterBefore(c):
    kbs = Kbs(config_object)
    kbs.installKbsMasterBefore()

@task
def validEtcd(c):
    etcd = Etcd(config_object)
    etcd.validEtcd()

@task
def installEtcdNodePrepare(c):
    etcd = Etcd(config_object)
    etcd.installEtcdNodePrepare()

@task
#install etcd cluster
def installEtcdNodeNormal(c, nodename):
    etcd = Etcd(config_object)
    etcd.installEtcdNodeNormal(nodename)

@task
#prepare works for every node
def installPrepareNodeNormal(c, nodename):
    prepare = Prepare(config_object)
    prepare.installNodeNormal(nodename)

@task
#install kubectl to node
def installKubectl(c):
    kbs = Kbs(config_object)
    kbs.installKubectl()

@task
#install coredns
def installCoredns(c):
    coredns = Coredns(config_object)
    coredns.installCoredns()

@task
#validate coredns
def validCoredns(c):
    coredns = Coredns(config_object)
    coredns.validCoredns()

@task
#delete coredns
def deleteCoredns(c):
    coredns = Coredns(config_object)
    coredns.deleteCoredns()

@task 
#install busybox to validate coredns
def installDemoBusybox(c):
    demo = Demo(config_object)
    demo.installDemoBusybox()

@task
#delete busybox demo
def deleteDemoBusybox(c):
    demo = Demo(config_object)
    demo.deleteDemoBusybox()

@task 
#install ingress demo
def installDemoIngress(c):
    demo = Demo(config_object)
    demo.installDemoIngress()

@task
#delete ingress demo
def deleteDemoIngress(c):
    demo = Demo(config_object)
    demo.deleteDemoIngress()

@task
#valid ingress demo
def validDemoIngress(c):
    demo = Demo(config_object)
    demo.validDemoIngress()

@task
#install ingress 
def installIngress(c):
    ingress = Ingress(config_object)
    ingress.installIngress()

@task
#validate ingress
def validIngress(c):
    ingress = Ingress(config_object)
    ingress.validIngress()

@task
#delete ingress
def deleteIngress(c):
    demo = Demo(config_object)
    demo.deleteDemoIngressHttps()
    demo.deleteDemoIngress()
    
    ingress = Ingress(config_object)
    ingress.deleteIngress()

@task
#config ingress https
def installDemoIngressHttps(c):
    demo = Demo(config_object)
    demo.installDemoIngressHttps()

@task
#valid ingress https
def validDemoIngressHttps(c):
    demo = Demo(config_object)
    demo.validDemoIngressHttps()

@task
#delete ingress demo https
def deleteDemoIngressHttps(c):
    demo = Demo(config_object)
    demo.deleteDemoIngressHttps()

