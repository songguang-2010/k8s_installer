#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

#scripts directory
scriptsPath=$(cd "$(dirname "$filePath")"; pwd)

#app root directory
rootPath=$(cd "$(dirname "$parent")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

# fab -c ${fabFile} sudo --cmd "systemctl stop etcd-node1" --nodename master1
#stop relative service if the service is running
# fab -c ${fabFile} sudo --cmd "systemctl stop etcd-node2" --nodename master2
#stop relative service if the service is running
# fab -c ${fabFile} sudo --cmd "systemctl stop etcd-node3" --nodename master3

#####etcd node1#####




#upload install script
# /bin/sh ${uploadFile} master1 ${configPath}/config_var.sh ${remoteTmpPath}/
# /bin/sh ${uploadFile} master1 ${filePath}/script_etcd_node1.sh ${remoteTmpPath}/

#exec install script for etcd node1
# /bin/sh ${execFile} master1 ${remoteTmpPath}/script_etcd_node1.sh

# cmdRemote="nohup systemctl restart etcd-node1 &> /dev/null &"
# fab -c ${fabFile} --pty sudo --cmd "${cmdRemote}" --nodename master1

fab -c ${fabFile} --pty installEtcdNodePrepare
fab -c ${fabFile} --pty installEtcdNodeNormal --nodename master1
fab -c ${fabFile} --pty installEtcdNodeNormal --nodename master2
fab -c ${fabFile} --pty installEtcdNodeNormal --nodename master3

# #download ca files form master1 to local
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/ca.csr ${tmpPath}
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/ca.pem ${tmpPath}
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/ca-key.pem ${tmpPath}
# #download etcd ca files form master1 to local
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/etcd.csr ${tmpPath}
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/etcd.pem ${tmpPath}
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/etcd-key.pem ${tmpPath}

#####etcd node2#####

#upload ca files to master2
# /bin/sh ${uploadFile} master2 ca.csr ${remoteSslPath}/
# /bin/sh ${uploadFile} master2 ca.pem ${remoteSslPath}/
# /bin/sh ${uploadFile} master2 ca-key.pem ${remoteSslPath}/
#upload etcd ca files to master2
# /bin/sh ${uploadFile} master2 etcd.csr ${remoteSslPath}/
# /bin/sh ${uploadFile} master2 etcd.pem ${remoteSslPath}/
# /bin/sh ${uploadFile} master2 etcd-key.pem ${remoteSslPath}/

#upload binary file for etcd processes
# /bin/sh ${uploadFile} master2 ${etcdBinPath}/etcd ${remoteBinPath}/
# /bin/sh ${uploadFile} master2 ${etcdBinPath}/etcdctl ${remoteBinPath}/
#upload etcd config file
# /bin/sh ${uploadFile} master2 ${etcdConfigPath}/etcd-node2.conf ${remoteCfgPath}
#upload systemd service file for etcd processes
# /bin/sh ${uploadFile} master2 ${etcdConfigPath}/etcd-node2.service ${remoteSystemdPath}
#upload install script
# /bin/sh ${uploadFile} master2 ${configPath}/config_var.sh ${remoteTmpPath}
# /bin/sh ${uploadFile} master2 ${filePath}/script_etcd_node2.sh ${remoteTmpPath}

#exec install script for etcd
# /bin/sh ${execFile} master2 ${remoteTmpPath}/script_etcd_node2.sh

# cmdRemote="nohup systemctl restart etcd-node2 &> /dev/null &"
# fab -c ${fabFile} --pty sudo --cmd "${cmdRemote}" --nodename master2

#####etcd node3#####

#upload ca files to master3
# /bin/sh ${uploadFile} master3 ca.csr ${remoteSslPath}/
# /bin/sh ${uploadFile} master3 ca.pem ${remoteSslPath}/
# /bin/sh ${uploadFile} master3 ca-key.pem ${remoteSslPath}/
#upload etcd ca files to master3
# /bin/sh ${uploadFile} master3 etcd.csr ${remoteSslPath}/
# /bin/sh ${uploadFile} master3 etcd.pem ${remoteSslPath}/
# /bin/sh ${uploadFile} master3 etcd-key.pem ${remoteSslPath}/

#upload binary file for etcd processes
# /bin/sh ${uploadFile} master3 ${etcdBinPath}/etcd ${remoteBinPath}
# /bin/sh ${uploadFile} master3 ${etcdBinPath}/etcdctl ${remoteBinPath}
#upload etcd config file
# /bin/sh ${uploadFile} master3 ${etcdConfigPath}/etcd-node3.conf ${remoteCfgPath}
#upload systemd service file for etcd processes
# /bin/sh ${uploadFile} master3 ${etcdConfigPath}/etcd-node3.service ${remoteSystemdPath}
#upload install script
# /bin/sh ${uploadFile} master3 ${configPath}/config_var.sh ${remoteTmpPath}
# /bin/sh ${uploadFile} master3 ${filePath}/script_etcd_node3.sh ${remoteTmpPath}

#exec install script for etcd
# /bin/sh ${execFile} master3 ${remoteTmpPath}/script_etcd_node3.sh

# cmdRemote="nohup systemctl restart etcd-node3 &> /dev/null &"
# fab -c ${fabFile} --pty sudo --cmd "${cmdRemote}" --nodename master3 
