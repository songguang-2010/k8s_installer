#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} installDashboard

# load config items
# . ${configPath}/config_var.sh

#delete old role binding in master1
# cmdRemote="kubectl delete clusterrolebinding/kubelet-bootstrap"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#create role binding in master1
# cmdRemote="kubectl create clusterrolebinding kubelet-bootstrap"
# cmdRemote="${cmdRemote} --clusterrole=system:node-bootstrapper"
# cmdRemote="${cmdRemote} --user=kubelet-bootstrap"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#upload
# /bin/sh ${uploadFile} master1 ${filePath}/dashboard-rbac.yaml ${remotePluginPath}/dashboard/
# /bin/sh ${uploadFile} master1 ${filePath}/dashboard-secret.yaml ${remotePluginPath}/dashboard/
# /bin/sh ${uploadFile} master1 ${filePath}/dashboard-configmap.yaml ${remotePluginPath}/dashboard/
# /bin/sh ${uploadFile} master1 ${filePath}/dashboard-controller.yaml ${remotePluginPath}/dashboard/
# /bin/sh ${uploadFile} master1 ${filePath}/dashboard-service.yaml ${remotePluginPath}/dashboard/
# /bin/sh ${uploadFile} master1 ${filePath}/kubernetes-dashboard.yaml ${remotePluginPath}/dashboard/

#install
# cmdRemote="kubectl create -f ${remotePluginPath}/dashboard/dashboard-rbac.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl create -f ${remotePluginPath}/dashboard/dashboard-secret.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl create -f ${remotePluginPath}/dashboard/dashboard-configmap.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl create -f ${remotePluginPath}/dashboard/dashboard-controller.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl create -f ${remotePluginPath}/dashboard/dashboard-service.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl apply -f ${remotePluginPath}/dashboard/kubernetes-dashboard.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1


