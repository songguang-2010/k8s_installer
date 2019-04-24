#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
# parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
# rootPath=$(cd "$(dirname "$parentPath")"; pwd)

# . ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

#####master1#####
/bin/sh ${filePath}/install_prepare_node_normal.sh master1

#####master2#####
/bin/sh ${filePath}/install_prepare_node_normal.sh master2

#####master3#####
/bin/sh ${filePath}/install_prepare_node_normal.sh master3

#####node1#####
/bin/sh ${filePath}/install_prepare_node_normal.sh node1

/bin/sh ${filePath}/install_prepare_node_normal.sh node2
