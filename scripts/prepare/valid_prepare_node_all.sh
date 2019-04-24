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

#exec command on remote node
echo "check firewalld status on master1: "
cmdRemote="systemctl status firewalld"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename master1
echo "check docker status on master1: "
cmdRemote="systemctl status docker"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename master1

echo "check firewalld status on master2: "
cmdRemote="systemctl status firewalld"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename master2
echo "check docker status on master2: "
cmdRemote="systemctl status docker"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename master2

echo "check firewalld status on master3: "
cmdRemote="systemctl status firewalld"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename master3
echo "check docker status on master3: "
cmdRemote="systemctl status docker"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename master3

echo "check firewalld status on node1: "
cmdRemote="systemctl status firewalld"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename node1
echo "check docker status on node1: "
cmdRemote="systemctl status docker"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename node1

echo "check docker version on node1: "
cmdRemote="docker --version"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename node1

echo "check docker version on node2: "
cmdRemote="docker --version"
fab -c ${fabFileCommon} sudo --cmd "${cmdRemote}" --nodename node2

