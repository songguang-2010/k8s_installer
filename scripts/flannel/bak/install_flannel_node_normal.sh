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
# load config items
. ${configPath}/config_var.sh

#stop relative service if the service is running
fab -c ${fabFile} sudo --cmd "systemctl stop flanneld" --nodename ${nodeName}

#download ca files form master1 to local
/bin/sh ${downloadFile} master1 ${remoteSslPath}/ca.csr ${tmpPath}/
/bin/sh ${downloadFile} master1 ${remoteSslPath}/ca.pem ${tmpPath}/
/bin/sh ${downloadFile} master1 ${remoteSslPath}/ca-key.pem ${tmpPath}/
#download etcd ca files form master1 to local
/bin/sh ${downloadFile} master1 ${remoteSslPath}/etcd.csr ${tmpPath}/
/bin/sh ${downloadFile} master1 ${remoteSslPath}/etcd.pem ${tmpPath}/
/bin/sh ${downloadFile} master1 ${remoteSslPath}/etcd-key.pem ${tmpPath}/

#upload ca files to node
/bin/sh ${uploadFile} ${nodeName} ca.csr ${remoteSslPath}/
/bin/sh ${uploadFile} ${nodeName} ca.pem ${remoteSslPath}/
/bin/sh ${uploadFile} ${nodeName} ca-key.pem ${remoteSslPath}/
/bin/sh ${uploadFile} ${nodeName} etcd.csr ${remoteSslPath}/
/bin/sh ${uploadFile} ${nodeName} etcd.pem ${remoteSslPath}/
/bin/sh ${uploadFile} ${nodeName} etcd-key.pem ${remoteSslPath}/

#upload binary file 
/bin/sh ${uploadFile} ${nodeName} ${flannelBinPath}/flanneld ${remoteBinPath}
/bin/sh ${uploadFile} ${nodeName} ${flannelBinPath}/mk-docker-opts.sh ${remoteBinPath}

#upload config file
/bin/sh ${uploadFile} ${nodeName} ${flannelConfigPath}/flanneld.conf ${remoteCfgPath}
#upload systemd service file 
/bin/sh ${uploadFile} ${nodeName} ${flannelConfigPath}/flanneld.service ${remoteSystemdPath}
/bin/sh ${uploadFile} ${nodeName} ${flannelConfigPath}/docker.service ${remoteSystemdPath}

fab -c ${fabFile} sudo --cmd "systemctl daemon-reload" --nodename ${nodeName}
fab -c ${fabFile} sudo --cmd "systemctl enable flanneld" --nodename ${nodeName}
fab -c ${fabFile} --pty sudo --cmd "nohup systemctl restart flanneld &> /dev/null &" --nodename ${nodeName}
fab -c ${fabFile} sudo --cmd "systemctl status flanneld" --nodename ${nodeName}

echo "sleep 5 seconds ..."
fab -c ${fabFile} sudo --cmd "sleep 5" --nodename ${nodeName}
fab -c ${fabFile} sudo --cmd "systemctl restart docker" --nodename ${nodeName}


