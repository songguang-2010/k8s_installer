#!/bin/sh

if [ -z $1 ]
then
  echo "node name is missing"
  exit 1
fi

nodeName=$1

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} --pty installCniNodeNormal --nodename ${nodeName}

# load config items
# . ${configPath}/config_var.sh

# #stop relative service if the service is running
# fab -c ${fabFile} sudo --cmd "systemctl stop kube-kubelet" --nodename ${nodeName}

# # upload cni files
# /bin/sh ${uploadFile} ${nodeName} ${cniBinPath}/loopback ${remoteCniBinPath}/
# /bin/sh ${uploadFile} ${nodeName} ${cniBinPath}/portmap ${remoteCniBinPath}/
# /bin/sh ${uploadFile} ${nodeName} ${cniConfigPath}/99-loopback.conf ${remoteCniCfgPath}/

# #upload kubelet service config file for cni
# fab -c ${parentPath}/fabfile_kbs uploadCniFiles --nodename ${nodeName}

# echo "systemd daemon reload ..."
# cmdRemote="systemctl daemon-reload"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename ${nodeName}

# echo "restart kubelet service ..."
# cmdRemote="systemctl restart kube-kubelet.service"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename ${nodeName}
# echo "check kubelet service ..."
# cmdRemote="systemctl status kube-kubelet.service"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename ${nodeName}



