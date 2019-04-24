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
scriptsPath=$(cd "$(dirname "$filePath")"; pwd)

# 在远端主机执行命令
echo "list keys in etcd: "
cmdValid0=" /opt/kubernetes/bin/etcdctl"
cmdValid1=" --endpoints https://172.18.100.47:2379,https://172.18.100.48:2379,https://172.18.100.49:2379"
cmdValid2=" --ca-file=/opt/kubernetes/ssl/ca.pem"
cmdValid3=" --cert-file=/opt/kubernetes/ssl/etcd.pem"
cmdValid4=" --key-file=/opt/kubernetes/ssl/etcd-key.pem"
cmdValid5=" ls / -r"
cmdValid="ETCDCTL_API=2 ${cmdValid0} ${cmdValid1} ${cmdValid2} ${cmdValid3} ${cmdValid4} ${cmdValid5}"
fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValid}" --nodename master1  

echo "get network config key of flannel in etcd: "
cmdValid5=" get /coreos.com/network/config"
cmdValid="ETCDCTL_API=2 ${cmdValid0} ${cmdValid1} ${cmdValid2} ${cmdValid3} ${cmdValid4} ${cmdValid5}"
fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValid}" --nodename master1

echo "list ips: "
fab -c ${scriptsPath}/common/fabfile sudo --cmd "ip a" --nodename ${nodeName} 


#进入一个节点，访问另一个节点的docker0 IP
#ping 172.17.56.1