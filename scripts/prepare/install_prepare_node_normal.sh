#!/bin/sh

if [ -z $1 ]
then
  echo "node name is missing"
  exit 1
fi

nodeName=$1

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

fab -c ${fabFile} installPrepareNodeNormal --nodename ${nodeName}

#upload install script
# /bin/sh ${uploadFile} ${nodeName} ${configPath}/config_var.sh ${remoteTmpPath}/
# /bin/sh ${uploadFile} ${nodeName} ${filePath}/script_prepare_node_normal.sh ${remoteTmpPath}/

#exec install script 
# /bin/sh ${execFile} ${nodeName} ${remoteTmpPath}/script_prepare_node_normal.sh