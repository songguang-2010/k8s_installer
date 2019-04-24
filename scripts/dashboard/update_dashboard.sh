#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

#parent directory
scriptsPath=$(cd "$(dirname "$filePath")"; pwd)

#delete dashboard pods and services 
cmdRemote="${remoteBinPath}/kubectl -n kube-system delete \$(${remoteBinPath}/kubectl -n kube-system get pod -o name | grep dashboard)"
fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="kubectl -n kube-system delete \$(kubectl -n kube-system get svc -o name | grep dashboard)"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1
