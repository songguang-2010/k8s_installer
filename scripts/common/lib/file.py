#!/usr/bin/env python
# coding:utf-8
# -*- coding: UTF-8 -*-

# 该脚本提供了有关文件操作的一些工具函数

import os.path


class File(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def read_line_first(filename):
        # 从文件中读取第一行的内容, 无论是空行还是到达文件末尾还是文件不存在, 都返回False
        # 如果文件不存在
        if not os.path.isfile(filename):
            # raise IOError(filename+" not exists")
            return False
        f = open(filename, "r")
        line = f.readline()
        f.close()
        # 判断是否到达文件尾部
        if not line:
            return False
        # 判断是否是空行
        line = line.strip()
        if not line:
            return False
        # 返回正常数据行
        return line

    @staticmethod
    def append_line(filename, line):
        # 附加一行内容到文件的末尾
        f = open(filename, "a")
        f.write(line)
        f.write('\n')
        f.close()

    @staticmethod
    def del_line_by_str(filename, content):
        # 根据指定的字符串内容, 删除指定文件中的指定的行,注意此函数处理的文件不应该过大
        if not os.path.isfile(filename):
            raise IOError(filename+" not exists")
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        # 文件内容的备份容器, 如果找到了匹配项目, 则该容器中不包含匹配项目
        lines_bak = []
        # 是否找到匹配项目的标记, 默认为没有找到
        found = False
        # 循环遍历发现匹配项目
        for line in lines:
            if line.startswith(content):
                found = True
                continue
            else:
                lines_bak.append(line)
        # 如果找到了匹配项目, 则重写文件
        if found:
            f = open(filename, "w")
            f.writelines(lines_bak)
            f.close()

    @staticmethod
    def move_line_by_str(filename_src, filename_des, content):
        # 根据给定的字符串内容, 在源文件中删除对应的行, 并将其追加写入到目标文件中
        # 追加内容到指定文件中
        File.append_line(filename_des, content)
        # 根据指定的内容, 从指定的文件中删除指定的行
        File.del_line_by_str(filename_src, content)