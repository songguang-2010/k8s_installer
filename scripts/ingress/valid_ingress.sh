#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} validIngress

# load config items
# . ${configPath}/config_var.sh

# #get namespaces
# cmdRemote="${remoteBinPath}/kubectl get ns"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #get pod list in namespace ingress-nginx
# cmdRemote="${remoteBinPath}/kubectl get rs,pods,svc -n ingress-nginx -o wide"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #get pod list in namespace default
# cmdRemote="${remoteBinPath}/kubectl get rs,pods,svc -n default -o wide"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #get process list listenning on 80 and 443 on target node
# cmdRemote="netstat -tnlp | egrep \"80|443\""
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename node1

#test myapp service cluterip in deploy node
#curl {clusterIp}

# #get ingress
# cmdRemote="${remoteBinPath}/kubectl get ingress"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#test domain by curl after set hosts to parse domain name to ip
#curl {domainName}

# #describe inress
# cmdRemote="${remoteBinPath}/kubectl describe ingress simple-fanout-example"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#get pod in namespace ingress-nginx, and execute command in it to check nginx configure contents
# cmdRemote="kubectl get pod -n ingress-nginx | grep nginx-ingress-controller | awk '{print \$1}'"
# cmdRemote="kubectl exec \$(${cmdRemote}) -n ingress-nginx -- cat nginx.conf"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1