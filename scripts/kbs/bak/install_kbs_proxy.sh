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

# . ${rootPath}/scripts/common/constant.sh
# . ${configPath}/config_var.sh

# #download proxy cert files from master1
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/kube-proxy.csr ${tmpPath}/
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/kube-proxy.pem ${tmpPath}/
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/kube-proxy-key.pem ${tmpPath}/

# #download proxy kubeconfig files from master1
# /bin/sh ${downloadFile} master1 ${remoteCfgPath}/kube-proxy.kubeconfig ${tmpPath}/

#####kubernetes node1#####

# #stop relative service if the service is running
# fab -c ${fabFile} sudo --cmd "systemctl stop kube-proxy" --nodename ${nodeName}

# #upload binary file for kube processes
# /bin/sh ${uploadFile} ${nodeName} ${kbsBinPath}/kube-proxy ${remoteBinPath}

# #upload proxy cert files to node1
# /bin/sh ${uploadFile} ${nodeName} kube-proxy.pem ${remoteSslPath}/

# #upload proxy kubeconfig files to node1
# /bin/sh ${uploadFile} ${nodeName} kube-proxy.kubeconfig ${remoteCfgPath}/

# #upload systemd service files to node1
# /bin/sh ${uploadFile} ${nodeName} ${kbsConfigPath}/kube-proxy.service ${remoteSystemdPath}/

# #upload proxy service config file
# fab -c ${parentPath}/fabfile_kbs uploadProxyFiles --nodename ${nodeName}

# echo "systemd daemon reload ..."
# cmdRemote="systemctl daemon-reload"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename ${nodeName}
# echo "enable proxy service ..."
# cmdRemote="systemctl enable kube-proxy.service"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename ${nodeName}
# echo "restart proxy service ..."
# cmdRemote="systemctl restart kube-proxy.service"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename ${nodeName}
# echo "check proxy service ..."
# cmdRemote="systemctl status kube-proxy.service"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename ${nodeName}












