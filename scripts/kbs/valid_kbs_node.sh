#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

fab -c ${fabFile} --pty validKbsNode

# echo "restart kube apiserver ..."
# cmdRemote="systemctl restart kube-apiserver"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# echo "show csr info: "
# fab -c ${fabFile} sudo --cmd "${remoteBinPath}/kubectl get csr" --nodename master1  
# echo "pass tls request: "
# cmd="${remoteBinPath}/kubectl get csr | grep 'Pending' | awk 'NR>0 {print \$1}' | xargs ${remoteBinPath}/kubectl certificate approve"
# fab -c ${fabFile} sudo --cmd "${cmd}" --nodename master1 

# #delete old anonymous role binding in master1
# cmdRemote="${remoteBinPath}/kubectl delete clusterrolebinding/cluster-system-anonymous"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #create role binding in master1
# cmdRemote="${remoteBinPath}/kubectl create clusterrolebinding cluster-system-anonymous"
# cmdRemote="${cmdRemote} --clusterrole=cluster-admin"
# cmdRemote="${cmdRemote} --user=system:anonymous"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# echo "show cluster nodes info: "
# cmdRemote="${remoteBinPath}/kubectl get node"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1  

# #uninstall old nginx pod and service
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remoteDemoPath}/nginx-demo-deployment.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1 

# #upload nginx-demo-deployment.yaml to master
# /bin/sh ${uploadFile} master1 ${filePath}/nginx-demo-deployment.yaml ${remoteDemoPath}/

# # create pod
# cmdRemote="${remoteBinPath}/kubectl apply -f ${remoteDemoPath}/nginx-demo-deployment.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# expose service
# kubectl expose deployment nginx --port=88 --target-port=80 --type=NodePort

# # list pod and service
# cmdRemote="${remoteBinPath}/kubectl get pod,svc -o wide"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# visit service web
# http://{nodeIp}:{exposePort}

#list logs by pod name
# kubectl logs {podName}
# cmdRemote="${remoteBinPath}/kubectl get pod,svc -o wide"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#show clusterrolebinding by cluster role name
# kubectl get clusterrolebinding/{clusterRole} -n kube-system -o yaml

#show clusterrole's privileges by cluster role name
# kubectl get clusterrole/{clusterRole} -n kube-system -o yaml

#list clusterroles
# kubectl get clusterroles