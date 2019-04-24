#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} installCoredns

# load config items
# . ${configPath}/config_var.sh

# #upload
# /bin/sh ${uploadFile} master1 ${filePath}/coredns-rbac.yaml ${remotePluginPath}/coredns/
# /bin/sh ${uploadFile} master1 ${filePath}/coredns-sa.yaml ${remotePluginPath}/coredns/
# /bin/sh ${uploadFile} master1 ${filePath}/coredns-configmap.yaml ${remotePluginPath}/coredns/
# /bin/sh ${uploadFile} master1 ${filePath}/coredns-deployment.yaml ${remotePluginPath}/coredns/
# /bin/sh ${uploadFile} master1 ${filePath}/coredns-service.yaml ${remotePluginPath}/coredns/
# /bin/sh ${uploadFile} master1 ${filePath}/kubernetes-coredns.yaml ${remotePluginPath}/coredns/

# #install
# cmdRemote="${remoteBinPath}/kubectl create -f ${remotePluginPath}/coredns/coredns-rbac.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl create -f ${remotePluginPath}/coredns/coredns-sa.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl create -f ${remotePluginPath}/coredns/coredns-configmap.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl create -f ${remotePluginPath}/coredns/coredns-deployment.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl create -f ${remotePluginPath}/coredns/coredns-service.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl apply -f ${remotePluginPath}/coredns/kubernetes-coredns.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1


