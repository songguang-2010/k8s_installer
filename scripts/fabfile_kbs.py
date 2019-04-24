#!/usr/bin/env python3
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本使用fabric api, 在本地操作远端主机资源
# 该脚本主要负责以下功能：
#
# 1.在远端主机上以sudo权限执行指定的命令

import sys
import os.path
import datetime
from fabric import task
from fabric import Connection
from invocations.console import confirm

# 获得当前文件所在目录
file_path = os.path.dirname(os.path.realpath(__file__))

# 获得应用根目录
app_path = os.path.dirname(file_path)

lib_path = os.path.abspath(file_path)
sys.path.append(lib_path)

# 导入自定义工具库
from lib.remote import *
from lib.xmlFile import *

# 远端主机节点文件
node_file = app_path+"/config/config_node.xml"
# 解析xml远端主机信息文件
node_object = XmlFile(node_file)

# 用于登录远程主机的账户信息
# env.hosts = []
# env.hosts.append(hostname)
class env(object):
    host = ""
    gateway = ""
    user = ""
    password = ""

# conn = Connection(env.host, user = env.user, connect_kwargs={"password": env.password})

def getEnv(nodename):
    node_data = node_object.get_node_by_attr("name", nodename)
    hostname = node_data.get('hostname')
    gateway = node_data.get('gateway')
    username = node_data.get('username')
    password = node_data.find('password').text
    # 判断是否存在堡垒机
    if gateway != "":
        env.gateway = gateway
    env.host = hostname
    env.user = username
    env.password = password

    return env

@task
def uploadApiserverFiles(c, nodename):
    # 上传apiserver相关文件到远端主机
    node_env = getEnv(nodename)

    # 初始化远程工具对象
    robj = Remote(node_env)

    

    print("Upload Success.")

@task
def uploadCniFiles(c, nodename):
    # 上传kublete相关文件到远端主机
    node_env = getEnv(nodename)

    # 初始化远程工具对象
    robj = Remote(node_env)

    

    print("Upload Success.")

@task
def uploadKubeletFiles(c, nodename):
    # 上传kublete相关文件到远端主机
    node_env = getEnv(nodename)

    # 初始化远程工具对象
    robj = Remote(node_env)

    

    print("Upload Success.")

@task
def uploadProxyFiles(c, nodename):
    # 上传kublete相关文件到远端主机
    node_env = getEnv(nodename)

    # 初始化远程工具对象
    robj = Remote(node_env)

    

    print("Upload Success.")


