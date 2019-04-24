#!/usr/bin/env python3
# coding:utf-8
# -*- coding: UTF-8 -*-

import copy
import os

# 导入自定义工具库
# lib_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(lib_path)
from lib.remote import Remote
from lib.xmlFile import XmlFile

class Base(object):
    def __init__(self, config_object):
        self.config_object = config_object
        env_data = config_object.get_node_by_attr("name", "env")
        self.mode = env_data.find('mode').text

        self.path_data = self.config_object.get_node_by_attr("name", "path")

        # 获得当前文件所在目录
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        # 获得应用根目录
        self.app_path = os.path.dirname(os.path.dirname(os.path.dirname(self.file_path)))

        # 远端主机节点文件
        if self.mode=="dev":
            self.node_file = self.app_path+"/config/config_node_dev.xml"
        else:
            self.node_file = self.app_path+"/config/config_node_production.xml"

        # 解析xml远端主机信息文件
        self.node_object = XmlFile(self.node_file)

    def __del__(self):
        pass

    def getLocalPath(self, tagname):
        return self.app_path+"/"+self.path_data.find(tagname).text

    def getRemotePath(self, tagname):
        return self.path_data.find(tagname).text

    def getEnv(self, nodename):
        node_data = self.node_object.get_node_by_attr("name", nodename)

        # 用于登录远程主机的账户信息
        class env(object):
            host = ""
            gateway = ""
            user = ""
            password = ""
            address = ""

        # 是否存在堡垒机
        env.gateway = node_data.get('gateway')
        if env.gateway == "":
            env.gateway = None
        env.host = node_data.get('hostname')
        env.user = node_data.get('username')
        env.password = node_data.find('password').text
        env.address = node_data.get('address')
        return copy.deepcopy(env)
