#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

#scripts directory
scriptsPath=$(cd "$(dirname "$filePath")"; pwd)

fab -c ${scriptsPath}/common/fabfile validEtcd

# cmdRemote="systemctl status etcd"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master1
# cmdRemote="systemctl status etcd"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master2
# cmdRemote="systemctl status etcd"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdRemote}" --nodename master3

# 在远端主机执行命令
# cmdValid0=" /opt/kubernetes/bin/etcdctl"
# cmdValid1=" --endpoints https://192.168.2.231:2379,https://192.168.2.232:2379,https://192.168.2.233:2379"
# cmdValid1=" --endpoints https://172.18.100.47:2379,https://172.18.100.48:2379,https://172.18.100.49:2379"
# cmdValid2=" --cacert=/opt/kubernetes/ssl/ca.pem"
# cmdValid3=" --cert=/opt/kubernetes/ssl/etcd.pem"
# cmdValid4=" --key=/opt/kubernetes/ssl/etcd-key.pem"
# cmdValidVersion3="ETCDCTL_API=3 ${cmdValid0} ${cmdValid1} ${cmdValid2} ${cmdValid3} ${cmdValid4}"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValidVersion3} endpoint health" --nodename master1 
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValidVersion3} endpoint hashkv" --nodename master1
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValidVersion3} member list" --nodename master1 

# cmdValid2_v2=" --ca-file=/opt/kubernetes/ssl/ca.pem"
# cmdValid3_v2=" --cert-file=/opt/kubernetes/ssl/etcd.pem"
# cmdValid4_v2=" --key-file=/opt/kubernetes/ssl/etcd-key.pem"
# cmdValidVersion2="ETCDCTL_API=2 ${cmdValid0} ${cmdValid1} ${cmdValid2_v2} ${cmdValid3_v2} ${cmdValid4_v2}"
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValidVersion2} cluster-health" --nodename master1 
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValidVersion2} member list" --nodename master1
# fab -c ${scriptsPath}/common/fabfile sudo --cmd "${cmdValidVersion2} ls / -r" --nodename master1