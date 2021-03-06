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

fab -c ${fabFile} installWeaveNodeNormal --nodename ${nodeName}

# load config items
# . ${configPath}/config_var.sh

# #install bridge tools
# cmdRemote="yum install -y bridge-utils"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename ${nodeName}

