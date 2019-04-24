#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} deleteIngress

# load config items
# . ${configPath}/config_var.sh

# #delete ingress
# echo "delete ingress ..."
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/ingress/mandatory.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #delete ingress backend
# echo "delete ingress backend demo ..."
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/ingress/nginx-ingress-backend.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #delete ingress rules
# echo "delete ingress rules ..."
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/ingress/nginx-ingress-rules.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #delete ingress rules of https
# echo "delete ingress rules of https ..."
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/ingress/nginx-ingress-rules-https.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1