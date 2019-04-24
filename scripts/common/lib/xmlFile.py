#!/usr/bin/env python
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本提供了有关xml文件操作的一些工具函数

# 导入xml解析库
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# 导入系统库
import sys

import os.path

# 导入自定义工具库
from lib.file import File


class XmlFile(File):
    def __init__(self, file_path):
        File.__init__(self)
        self.file_path = file_path
        # 解析xml主机信息文件
        try:
            # 打开xml文档
            self.tree_node = ET.parse(file_path)
            
        except Exception as e:
            print(e)
            print("Error:cannot parse file:%s." % file_path)
            sys.exit(1)

    def __del__(self):
        File.__del__(self)

    def get_root_node(self):
        # 获得root节点 
        return self.tree_node.getroot()
    
    def get_node_by_attr(self, attr_key, attr_value):
        # 获得指定属性的节点
        pathString = ".//*[@%s='%s']" % (attr_key, attr_value)
        # print(pathString)
        return self.tree_node.find(pathString)
