#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

#parent directory
parent=$(dirname "$filepath")

# 上传到远端主机
fab -c ${filePath}/fabfile_kbs uploadKubeletFiles --nodename node1
