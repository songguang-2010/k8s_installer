#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

#prepare for working node

fab -c ${fabFile} installKbsNodeBefore
fab -c ${fabFile} installKbsNodeNormal --nodename node1
fab -c ${fabFile} installKbsNodeNormal --nodename node2

