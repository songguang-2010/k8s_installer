#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

kubectlFile="${rootPath}/resource/kubernetes/server/bin/kubectl"

${kubectlFile}  get pod,svc -n kube-system -o wide | grep grafana

# corednsConfigPath="${rootPath}/config/coredns"

# secretName=$(${kubectlFile} -n kube-system get secret | grep kubernetes-dashboard-token | awk '{print $1}')

# ${kubectlFile} -n kube-system describe secret ${secretName} 
