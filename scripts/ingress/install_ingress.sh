#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} installIngress

# load config items
# . ${configPath}/config_var.sh

# #remove
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/ingress/mandatory.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# #upload yaml file
# /bin/sh ${uploadFile} master1 ${filePath}/mandatory.yaml ${remotePluginPath}/ingress/
# #install
# cmdRemote="${remoteBinPath}/kubectl apply -f ${remotePluginPath}/ingress/mandatory.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1


# # remove ingress backend
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/ingress/nginx-ingress-backend.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# #upload ingress backend
# /bin/sh ${uploadFile} master1 ${filePath}/nginx-ingress-backend.yaml ${remotePluginPath}/ingress/
# #install ingress backend
# cmdRemote="${remoteBinPath}/kubectl apply -f ${remotePluginPath}/ingress/nginx-ingress-backend.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# # remove ingress rules
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/ingress/nginx-ingress-rules.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# #upload ingress rules
# /bin/sh ${uploadFile} master1 ${filePath}/nginx-ingress-rules.yaml ${remotePluginPath}/ingress/
# #install ingress rules
# cmdRemote="${remoteBinPath}/kubectl apply -f ${remotePluginPath}/ingress/nginx-ingress-rules.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
