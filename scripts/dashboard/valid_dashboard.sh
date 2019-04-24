#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} validDashboard

# load config items
# . ${configPath}/config_var.sh

#valid

# #list pod and service 
# cmdRemote="${remoteBinPath}/kubectl get pod,svc -n kube-system -o wide"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #cluster info
# cmdRemote="${remoteBinPath}/kubectl cluster-info -n kube-system"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#visit address in explorer
# https://{masterIp}:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login

# #list tokens of kube-system namespaces
# cmdRemote="${remoteBinPath}/kubectl -n kube-system get secret"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #get token name to login
# cmdRemote="${remoteBinPath}/kubectl -n kube-system get secret | grep kubernetes-dashboard-token | awk '{print \$1}'"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# cmdRemote="${remoteBinPath}/kubectl -n kube-system describe secret \$(${cmdRemote})"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1



