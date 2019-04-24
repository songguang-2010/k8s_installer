#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} validCoredns

# load config items
# . ${configPath}/config_var.sh

#valid

# #show pod list
# echo "show pod list in default ..."
# cmdRemote="${remoteBinPath}/kubectl get pods"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# echo "show service list in default ..."
# cmdRemote="${remoteBinPath}/kubectl get services"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #show pod list
# echo "show pod list in kube-system ..."
# cmdRemote="${remoteBinPath}/kubectl get pods -n kube-system"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #show pod list
# echo "show service list in kube-system ..."
# cmdRemote="${remoteBinPath}/kubectl get services -n kube-system"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #uninstall old service
# echo "remove busybox container ..."
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/coredns/busybox.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #upload
# echo "upload busybox yaml ..."
# /bin/sh ${uploadFile} master1 ${filePath}/busybox.yaml ${remotePluginPath}/coredns/

# #install
# echo "create busybox container ..."
# cmdRemote="${remoteBinPath}/kubectl create -f ${remotePluginPath}/coredns/busybox.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# echo "sleep 5 seconds ..."
# sleep 5s

# #view
# echo "list pods of busybox ..."
# cmdRemote="${remoteBinPath}/kubectl get pods busybox"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #Verify that the search path and name server are set up
# echo "check content in resolv.conf ..."
# cmdRemote="${remoteBinPath}/kubectl exec busybox cat /etc/resolv.conf"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #exec cmd in busybox container terminal, and test dns service
# echo "test dns service in container busybox ..."
# cmdRemote="${remoteBinPath}/kubectl exec busybox -- nslookup kubernetes.default"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#查看日志信息
# for p in $(kubectl get pods --namespace=kube-system -l k8s-app=coredns -o name); do kubectl logs --namespace=kube-system $p; done

#查看pod中的所有容器
# kubectl describe {podName} -n {namespaceName}
#查看容器中以daemon形式运行的进程的输出
# kubectl attach {podName} -c {containerName} —namespace={namespaceName}
#查看coredns暴露的端点信息
# cmdRemote="kubectl get ep coredns -n kube-system"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1



