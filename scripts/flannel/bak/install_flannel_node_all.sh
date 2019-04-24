#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
. ${configPath}/config_var.sh

#prepare for flannel node

#delete old key
cmdRemote="ETCDCTL_API=2 /opt/kubernetes/bin/etcdctl"
cmdRemote="${cmdRemote} --endpoints ${ETCD_CLUSTER_SERVER}"
cmdRemote="${cmdRemote} --ca-file=${remoteSslPath}/ca.pem"
cmdRemote="${cmdRemote} --cert-file=${remoteSslPath}/etcd.pem"
cmdRemote="${cmdRemote} --key-file=${remoteSslPath}/etcd-key.pem"
cmdRemote="${cmdRemote} rm /coreos.com/network/config"
fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#add new key
cmdRemote="ETCDCTL_API=2 /opt/kubernetes/bin/etcdctl"
cmdRemote="${cmdRemote} --endpoints ${ETCD_CLUSTER_SERVER}"
cmdRemote="${cmdRemote} --ca-file=${remoteSslPath}/ca.pem"
cmdRemote="${cmdRemote} --cert-file=${remoteSslPath}/etcd.pem"
cmdRemote="${cmdRemote} --key-file=${remoteSslPath}/etcd-key.pem"
cmdRemote="${cmdRemote} set /coreos.com/network/config {\\\"Network\\\":\\\"${FLANNEL_IP_SECTION}\\\"\,\\\"Backend\\\":{\\\"Type\\\":\\\"vxlan\\\"\,\\\"DirectRouting\\\":true}}"
echo ${cmdRemote}
fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#####flannel node1#####
/bin/sh ${filePath}/install_flannel_node_normal.sh master1

#####flannel node2#####
/bin/sh ${filePath}/install_flannel_node_normal.sh node1

echo "sleep 5 seconds ..."
fab -c ${fabFile} sudo --cmd "sleep 5" --nodename master1
fab -c ${fabFile} sudo --cmd "systemctl restart docker" --nodename master1

echo "sleep 5 seconds ..."
fab -c ${fabFile} sudo --cmd "sleep 5" --nodename node1
fab -c ${fabFile} sudo --cmd "systemctl restart docker" --nodename node1
