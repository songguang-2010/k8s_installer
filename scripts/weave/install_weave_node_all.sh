#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} installWeaveNodeNormal --nodename node1
fab -c ${fabFile} installWeaveNodeNormal --nodename node2
fab -c ${fabFile} installWeaveNodeAfter

# load config items
# . ${configPath}/config_var.sh

# /bin/sh ${filePath}/install_weave_node_normal.sh node1

# #upload yaml file 
# /bin/sh ${uploadFile} master1 ${filePath}/weave.yaml ${remotePluginPath}/weave/

# #install weave plugin
# # yamlWeave="https://cloud.weave.works/k8s/net?k8s-version=\$(${remoteBinPath}/kubectl version | base64 | tr -d '\\\n')"
# cmdRemote="${remoteBinPath}/kubectl apply -f ${remotePluginPath}/weave/weave.yaml"
# # echo ${cmdRemote}
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1



