#!/bin/sh

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
fab -c ${scriptsPath}/common/fabfile sudo --cmd "ip a" --nodename master1
fab -c ${scriptsPath}/common/fabfile sudo --cmd "ip a" --nodename node1
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "ip a" --nodename node2

echo "get network config key of flannel in etcd: "
cmdValid5=" get /coreos.com/network/subnets/192.19.48.0-24"
cmdValid="ETCDCTL_API=2 ${cmdValid0} ${cmdValid1} ${cmdValid2} ${cmdValid3} ${cmdValid4} ${cmdValid5}"
fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValid}" --nodename master1

#进入一个节点，访问另一个节点的docker0 IP
#ping 172.17.56.1