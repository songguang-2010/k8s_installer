#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$filePath")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

# install prepare
/bin/sh ${filePath}/prepare/install_prepare_node_all.sh

# install etcd
/bin/sh ${filePath}/etcd/install_etcd.sh

# install master

# install kubectl

# install worker 

# install cni and weave

# install docker private registry

# install demo docker private

# install coredns

# install demo busybox

# install demo nginx

# install dashboard

# install ingress controller

# install metrics server

