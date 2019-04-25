#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} --pty installCniNodeNormal --nodename master1
fab -c ${fabFile} --pty installCniNodeNormal --nodename master2
fab -c ${fabFile} --pty installCniNodeNormal --nodename master3
fab -c ${fabFile} --pty installCniNodeNormal --nodename node1
fab -c ${fabFile} --pty installCniNodeNormal --nodename node2