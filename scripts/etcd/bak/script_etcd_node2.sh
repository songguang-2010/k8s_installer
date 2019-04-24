#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

# load config items
. ${filePath}/config_var.sh

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
# systemctl enable etcd-node2.service
# (nohup systemctl restart etcd-node2.service &) && sleep 1
