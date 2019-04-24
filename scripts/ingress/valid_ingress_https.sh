#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} validDemoIngressHttps

# load config items
# . ${configPath}/config_var.sh

# #get ingress
# cmdRemote="${remoteBinPath}/kubectl get ingress"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#test domain by curl after set hosts to parse domain name to ip
#curl https://{domainName}

# #describe ingress
# cmdRemote="${remoteBinPath}/kubectl describe ingress tls-example-ingress"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#get pod in namespace ingress-nginx, and execute command in it to check nginx configure contents
# cmdRemote="${remoteBinPath}/kubectl get pod -n ingress-nginx | grep nginx-ingress-controller | awk '{print \$1}'"
# cmdRemote="${remoteBinPath}/kubectl exec \$(${cmdRemote}) -n ingress-nginx -- cat nginx.conf"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1