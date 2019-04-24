#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

# load config items
. ${filePath}/config_var.sh

# generate ca root cert
# if [ -f "/opt/kubernetes/ssl/ca.pem" ]; then
#     rm /opt/kubernetes/ssl/ca.pem
# fi
# if [ -f "/opt/kubernetes/ssl/ca-key.pem" ]; then
#     rm /opt/kubernetes/ssl/ca-key.pem
# fi
# if [ -f "/opt/kubernetes/ssl/ca.csr" ]; then
#     rm /opt/kubernetes/ssl/ca.csr
# fi
# /usr/local/bin/cfssl gencert -initca /opt/kubernetes/ssl/ca-csr.json | /usr/local/bin/cfssljson -bare /opt/kubernetes/ssl/ca

#generate etcd cert for each node
# if [ -f "/opt/kubernetes/ssl/etcd.pem" ]; then
#     rm /opt/kubernetes/ssl/etcd.pem
# fi
# if [ -f "/opt/kubernetes/ssl/etcd-key.pem" ]; then
#     rm /opt/kubernetes/ssl/etcd-key.pem
# fi
# if [ -f "/opt/kubernetes/ssl/etcd.csr" ]; then
#     rm /opt/kubernetes/ssl/etcd.csr
# fi
# /usr/local/bin/cfssl gencert -ca=/opt/kubernetes/ssl/ca.pem -ca-key=/opt/kubernetes/ssl/ca-key.pem -config=/opt/kubernetes/ssl/ca-config.json -profile=kubernetes /opt/kubernetes/ssl/etcd-csr.json | /usr/local/bin/cfssljson -bare /opt/kubernetes/ssl/etcd

# open some ports
#firewall-cmd --zone=public --add-port=2379/tcp --permanent
#firewall-cmd --zone=public --add-port=2380/tcp --permanent
#firewall-cmd --zone=public --add-port=4001/tcp --permanent
# reload config
#firewall-cmd --reload
# check ports
#firewall-cmd --zone=public --list-ports --permanent

# rm old directory for cache deleteing
# if [ -n "$ETCD_DATA_DIR" ] && [ -d "$ETCD_DATA_DIR" ] && [ "$ETCD_DATA_DIR" != "/" ]; then
#     rm -rf ${ETCD_DATA_DIR}*
#     echo "cache files of etcd is removed ..."
#     ls -l ${ETCD_DATA_DIR}
# else
#     # make directory to be used to store etcd data
#     mkdir --mode=755 -p ${ETCD_DATA_DIR}
# fi

#systemd for etcd process
# systemctl daemon-reload
# systemctl enable etcd-node1.service
# (nohup systemctl restart etcd-node1.service &) && sleep 1
