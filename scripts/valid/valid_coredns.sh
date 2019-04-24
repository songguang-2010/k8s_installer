#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

kubectlFile="${rootPath}/resource/kubernetes/server/bin/kubectl"

${kubectlFile}  get pod,svc -n kube-system -o wide | grep dns

corednsConfigPath="${rootPath}/config/coredns"

${kubectlFile} create -f ${corednsConfigPath}/busybox.yaml

${kubectlFile}  get pod,svc -n kube-system -o wide | grep dns

${kubectlFile} exec busybox -- nslookup kubernetes