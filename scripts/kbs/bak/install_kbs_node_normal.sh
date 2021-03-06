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

# . ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

#install for node

#install kubelet
# /bin/sh ${filePath}/install_kbs_kubelet.sh ${nodeName}
#install proxy
# /bin/sh ${filePath}/install_kbs_proxy.sh ${nodeName}
