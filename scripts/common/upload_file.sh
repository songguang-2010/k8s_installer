#!/bin/sh

if [ -z $1 ]
then
  echo "node name is missing"
  exit 1
fi

nodeName=$1

if [ -z $2 ]
then
  echo "source file is missing"
  exit 1
fi

srcFile=$2

if [ -z $3 ]
then
  echo "destination path is missing"
  exit 1
fi

desDir=$3

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

#parent directory
parent=$(dirname "$filepath")

# 上传到远端主机
fab -c ${filePath}/fabfile_common upload --dirlocal ${srcFile} --dirdes ${desDir} --nodename ${nodeName}  
