#!/usr/bin/env python3
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本使用fabric api, 在本地操作远端主机资源
# 该脚本主要负责以下功能：
#
# 1.根据给定的文件路径, 上传文件到远程主机
# 2.根据给定的文件路径, 执行远端的文件
# 3.根据给定的文件路径, 进行远端文件的删除
# 4.根据给定的文件路径, 从远程主机下载文件

# from fabric import colors
# from fabric import api
# from fabric.context_managers import *
# from fabric.contrib.console import *
# from fabric.api import local
# from fabric.contrib.files import *
# import time
# from pathlib import Path
# import os
# from __future__ import with_statement
# import fabric
import traceback
import os
# import sys
from fabric import Connection
from patchwork.files import exists as fab_exists
from os.path import exists
from os.path import basename
# from fabric import context_managers

class Remote(object):
    def __init__(self, env):
        if env.gateway != None:
            self.gatewayConn = Connection(env.gateway, user=env.user, connect_kwargs={
                               "password": env.password})
            self.conn = Connection(env.address, user=env.user, gateway=self.gatewayConn, connect_kwargs={
                               "password": env.password})
        else:
            self.conn = Connection(env.host, user=env.user, connect_kwargs={
                               "password": env.password})
        # print('\n'.join(['%s:%s' % item for item in self.conn.__dict__.items()]))
        self.result = ""

    def __del__(self):
        pass

    def getResult(self):
        return self.result
        
    def mkdir(self, dir_remote):
        # 检查指定远程目录是否存在, 不存在则尝试创建
        if not self.checkpath(dir_remote):
            print("ready to mkdir: %s ..." % dir_remote)
            if self.conn.run("mkdir --mode=755 -p %s" % dir_remote).failed:
                return False
                
        return True

    def checkpath(self, filename):
        # print("check remote path %s ..." % filename)
        # 检查指定远程文件或目录是否存在
        if fab_exists(self.conn, filename) == True:
            # print("remote file '%s' exists ..." % filename)
            return True
        else:
            return False

    def rmfile(self, filename):
        # 删除指定远程文件或目录，略过根目录
        if filename == "/":
            return False

        if self.checkpath(filename):
            if self.conn.sudo("rm -rf %s" % filename).failed:
                return False
        return True

    def cleanup(self, dir_remote):
        if (dir_remote == "" or dir_remote == "/" or self.checkpath(dir_remote) == False):
            return False

        if self.conn.sudo("rm -rf %s" % (dir_remote+"/*")).failed:
            return False
            
        return True

    def cleanupLocal(self, dir_local, sudo = False):
        if (dir_local == "" or dir_local == "/" or self.checkpath(dir_local) == False):
            return False

        cmdLocal = "rm -rf %s" % (dir_local+"/*")

        if sudo == True:
            cmdLocal = "sudo -s " + cmdLocal

        if self.conn.local(cmdLocal).failed:
            return False
            
        return True

    # def rename(self, file_src, file_des):
    #     # 重命名指定远程文件或目录
    #     with settings(warn_only=True):
    #         if exists(file_src, True):
    #             sudo("mv %s %s" % (file_src, file_des))

    def upload(self, dir_local, dir_remote, force = False):
        # 上传文件到远程主机
        print("ready to upload file: %s" % dir_local)

        result_check = self.mkdir(dir_remote)
        if result_check == False:
            print("failed to mkdir: %s" % dir_remote)

        file_name = os.path.basename(dir_local)
        file_remote = dir_remote + file_name

        if self.checkpath(file_remote) == True and force == False:
            print("remote file exists, skip upload ...")
            return True

        try:
            self.conn.put(dir_local, dir_remote)
        except Exception:
            print("Exception: exception occurred when upload file ...")
            print(traceback.print_exc())
            return False
        
        # print '\n'.join(['%s:%s' % item for item in result.__dict__.items()])
        # print(result)
        # if result.failed:
        # abort("Aborting file upload task， task failed!")
        # else:
        print("end to upload.")
        # sudo("ls -l %s" % dir_remote)
        # 列表文件
        # self.conn.sudo("ls -l %s" % dir_remote)
        return True

    def download(self, dir_remote, dir_local):
        # 从远程主机下载文件
        print("ready to download file: %s " % dir_remote)

        if not exists(dir_local):
            print("ready to mkdir: %s ..." % dir_local)
            if self.conn.local("mkdir --mode=755 -p %s" % dir_local).failed:
                print("Error: failed to mkdir on local machine, path: %s" % dir_local)
                return False

        baseName = os.path.basename(dir_remote)
        fileLocal = dir_local+baseName
        if exists(fileLocal):
            print("local file exists, skip download ...")
            return True

        isOk = True

        try:
            f = open(fileLocal, 'wb')
            self.result = self.conn.get(dir_remote, f)
        except Exception:
            print("Exception: exception occurred when download file ...")
            print("File: "+dir_remote)
            print(traceback.print_exc())
            isOk = False
        finally:
            if f:
                print("ready to close file: "+fileLocal)
                f.close()

        # if self.result.failed:
        #     print("Error: failed to download file ...")
        #     print("File: "+dir_remote)
        #     return False
            # print('\n'.join(['%s:%s' % item for item in result.__dict__.items()]))

        print("end to download.")
        # 列表文件
        # self.conn.local("ls -l %s" % dir_local)

        return isOk

    def sudo(self, cmd):
        # 在远程主机上以sudo权限运行指定命令
        print("start super run ...")
        try:
            self.result = self.conn.sudo("%s" % cmd)
            if self.result.failed:
                print("Error: failed to execute remote command ...")
                print("Command: "+cmd)
                return False
        except Exception:
            print("Exception: exception occurred when executing remote command ...")
            print("Command: "+cmd)
            print(traceback.print_exc())
            return False
        print("end super run.")
        return True

    def run(self, cmd):
        # 在远程主机上以当前用户身份运行指定命令
        print("start run ...")
        try:
            self.result = self.conn.run("%s" % cmd)
            if self.result.failed:
                print("Error: failed to execute remote command ...")
                print("Command: "+cmd)
                return False
        except Exception:
            print("Exception: exception occurred when executing remote command ...")
            print("Command: "+cmd)
            return False
        print("end run.")
        return True

    def local(self, cmd):
        # 在本地主机上运行指定命令
        print("start run ...")
        self.result = self.conn.local("%s" % cmd)
        if self.result.failed:
            print("Error: failed to execute local command ...")
            return False
        print("end run.")
        return True

    # def run(self, cmd):
    #     # 在远程主机上运行指定命令
    #     with settings(warn_only=True):
    #         print yellow("start run ...")
    #         run("%s" % cmd)
    #         print yellow("end run ...")

    # def delete(self, dir_remote, filename):
    #     # 从远程主机上删除指定文件
    #     with settings(warn_only=True):
    #         print yellow("list files ...")
    #         sudo("ls -l %s" % dir_remote)
    #         print yellow("start delete ...")
    #         sudo("rm %s" % dir_remote+filename)
    #         print yellow("end delete ...")
    #         sudo("ls -l %s" % dir_remote)
