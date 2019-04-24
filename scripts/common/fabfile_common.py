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
import copy
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

# 获得当前文件所在目录
file_path = os.path.dirname(os.path.realpath(__file__))
# 获得应用根目录
app_path = os.path.dirname(os.path.dirname(file_path))

# 配置文件
config_file = app_path+"/config/config.xml"
config_object = XmlFile(config_file)

env_data = config_object.get_node_by_attr("name", "env")
mode = env_data.find('mode').text

# 远端主机节点文件
if mode=="dev":
    node_file = app_path+"/config/config_node_dev.xml"
else:
    node_file = app_path+"/config/config_node_production.xml"

# 解析xml远端主机信息文件
node_object = XmlFile(node_file)

def getEnv(nodename):
    node_data = node_object.get_node_by_attr("name", nodename)

    # 用于登录远程主机的账户信息
    class env(object):
        host = ""
        gateway = ""
        user = ""
        password = ""

    # 是否存在堡垒机
    env.gateway = node_data.get('gateway')
    if env.gateway == "":
        env.gateway = None
    env.host = node_data.get('hostname')
    env.user = node_data.get('username')
    env.password = node_data.find('password').text
    return copy.deepcopy(env)

@task
# 删除远端主机中指定文件
def rmRemoteFile(c, filename, nodename):
    # 初始化远程工具对象
    robj = Remote(getEnv(nodename))

    # 删除远程文件
    result = robj.rmfile(filename)
    if result==False:
        print("failed to delete remote file.")
        if not confirm("failed to delete remote file, Continue[Y/N]?"):
            return True
    else:
        print("succeed to delete remote file.")
    
    return True

@task
# 检查远端主机中指定文件或目录是否存在
def checkRemotePath(c, path, nodename):
    # 初始化远程工具对象
    robj = Remote(getEnv(nodename))

    # 下载文件到本地
    result = robj.checkpath(path)
    if result==False:
        print("Remote Path not exists.")
        if not confirm("Path not exists in remote machine, Continue[Y/N]?"):
            return True
    else:
        print("Remote Path exists.")
    
    return True

@task
# 在远端主机中运行指定命令
def sudo(c, cmd, nodename):

    # 初始化远程工具对象
    robj = Remote(getEnv(nodename))
    robj.sudo(cmd)

    print("Exec Success.")

@task
# 下载远端主机中指定文件
def download(c, dirremote, dirlocal, nodename):
    # 初始化远程工具对象
    robj = Remote(getEnv(nodename))

    # 下载文件到本地
    result = robj.download(dirremote, dirlocal)
    if result==False:
        print("Download Failed.")
        # if not confirm("Failed to download file, Continue[Y/N]?"):
            # return True
    else:
        print("Download Success.")
    
    return True

@task
# 上传本地文件到远端主机指定目录
def upload(c, dirlocal, dirdes, nodename):
    print(dirlocal)
    print(nodename)

    # 初始化远程工具对象
    robj = Remote(getEnv(nodename))

    # 上传文件到远程主机
    robj.upload(dirlocal, dirdes)

    print("Upload Success.")



