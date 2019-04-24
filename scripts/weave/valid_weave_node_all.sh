#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} validWeaveNodeAll

# # 在远端主机执行命令
# echo "list weave net pods: "
# cmdRemote="/opt/kubernetes/bin/kubectl get pods -n kube-system -l name=weave-net -o wide"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1

# # kubectl exec -n kube-system weave-net-kgfvp -c weave -- /home/weave/weave --local status
# cmdRemote="/opt/kubernetes/bin/kubectl  exec -n kube-system weave-net-kgfvp -c weave -- /home/weave/weave --local status"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1