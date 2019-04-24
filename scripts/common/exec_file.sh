#!/bin/sh

if [ -z $1 ]
then
  echo "node name is missing"
  exit 1
fi

nodeName=$1

if [ -z $2 ]
then
  echo "script file is missing"
  exit 1
fi

scriptFile=$2

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

#parent directory
parent=$(dirname "$filepath")

# 在远端主机执行命令
fab -c ${filePath}/fabfile_common sudo --cmd "/bin/sh ${scriptFile}" --nodename ${nodeName}  
