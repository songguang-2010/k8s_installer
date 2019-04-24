#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} deleteCoredns

# load config items
# . ${configPath}/config_var.sh

# #delete coredns resources 
# cmdRemote="${remoteBinPath}/kubectl delete -f /opt/kubernetes/addons/coredns/coredns-configmap.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl delete -f /opt/kubernetes/addons/coredns/coredns-deployment.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl delete -f /opt/kubernetes/addons/coredns/coredns-rbac.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl delete -f /opt/kubernetes/addons/coredns/coredns-sa.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl delete -f /opt/kubernetes/addons/coredns/coredns-service.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl delete -f /opt/kubernetes/addons/coredns/kubernetes-coredns.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
