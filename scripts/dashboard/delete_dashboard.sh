#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} deleteDashboard

#delete dashboard resources 
# cmdRemote="kubectl delete -f /opt/kubernetes/addons/dashboard/dashboard-configmap.yaml"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl delete -f /opt/kubernetes/addons/dashboard/dashboard-controller.yaml"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl delete -f /opt/kubernetes/addons/dashboard/dashboard-rbac.yaml"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl delete -f /opt/kubernetes/addons/dashboard/dashboard-secret.yaml"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl delete -f /opt/kubernetes/addons/dashboard/dashboard-service.yaml"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="${remoteBinPath}/kubectl delete -f /opt/kubernetes/addons/dashboard/kubernetes-dashboard.yaml"
# fab -c ${scriptsPath}/common/fabfile_common sudo --cmd "${cmdRemote}" --nodename master1
