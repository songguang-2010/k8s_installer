#!/bin/sh

if [ -z $1 ]
then
  echo "node name is missing"
  exit 1
fi

nodeName=$1

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$filePath")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

#execute install_prepare_node_normal.sh script
/bin/sh ${filePath}/prepare/install_prepare_node_normal.sh ${nodeName}
#reconfig etcd cert files
#.....
#execute install_kbs_node_normal.sh script
/bin/sh ${filePath}/kbs/install_kbs_node_normal.sh ${nodeName}
#install cni and weave
/bin/sh ${filePath}/cni/install_cni_node_normal.sh ${nodeName}
/bin/sh ${filePath}/weave/install_weave_node_normal.sh ${nodeName}
