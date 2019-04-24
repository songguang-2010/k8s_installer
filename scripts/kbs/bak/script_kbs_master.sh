#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)

# load config items
. ${filePath}/config_var.sh

#generate kubernetes cert for each node
# if [ -f "/opt/kubernetes/ssl/kubernetes.pem" ]; then
#     rm /opt/kubernetes/ssl/kubernetes.pem
# fi
# if [ -f "/opt/kubernetes/ssl/kubernetes-key.pem" ]; then
#     rm /opt/kubernetes/ssl/kubernetes-key.pem
# fi
# if [ -f "/opt/kubernetes/ssl/kubernetes.csr" ]; then
#     rm /opt/kubernetes/ssl/kubernetes.csr
# fi
# /usr/local/bin/cfssl gencert -ca=/opt/kubernetes/ssl/ca.pem -ca-key=/opt/kubernetes/ssl/ca-key.pem -config=/opt/kubernetes/ssl/ca-config.json -profile=kubernetes /opt/kubernetes/ssl/kubernetes-csr.json | /usr/local/bin/cfssljson -bare /opt/kubernetes/ssl/kubernetes

#modify hostname
# hostnamectl set-hostname k8s-master1

# verify
# openssl x509 -in /opt/kubernetes/ssl/kubernetes.pem -text -noout

#systemd for kubernetes process
# systemctl daemon-reload
# systemctl enable kube-apiserver
# systemctl restart kube-apiserver
# systemctl status kube-apiserver

# systemctl enable kube-controller-manager
# systemctl restart kube-controller-manager
# systemctl status kube-controller-manager

# systemctl enable kube-scheduler
# systemctl restart kube-scheduler
# systemctl status kube-scheduler

# #generate admin cert for each node
# if [ -f "/opt/kubernetes/ssl/admin.pem" ]; then
#     rm /opt/kubernetes/ssl/admin.pem
# fi
# if [ -f "/opt/kubernetes/ssl/admin-key.pem" ]; then
#     rm /opt/kubernetes/ssl/admin-key.pem
# fi
# if [ -f "/opt/kubernetes/ssl/admin.csr" ]; then
#     rm /opt/kubernetes/ssl/admin.csr
# fi
# /usr/local/bin/cfssl gencert -ca=/opt/kubernetes/ssl/ca.pem -ca-key=/opt/kubernetes/ssl/ca-key.pem -config=/opt/kubernetes/ssl/ca-config.json -profile=kubernetes /opt/kubernetes/ssl/admin-csr.json | /usr/local/bin/cfssljson -bare /opt/kubernetes/ssl/admin

#set cluster parameters
# /opt/kubernetes/bin/kubectl config set-cluster kubernetes \
#   --certificate-authority=/opt/kubernetes/ssl/ca.pem \
#   --embed-certs=true \
#   --server=${KUBECTL_SERVER}

# #set client authority parameters
# /opt/kubernetes/bin/kubectl config set-credentials admin \
#   --client-certificate=/opt/kubernetes/ssl/admin.pem \
#   --embed-certs=true \
#   --client-key=/opt/kubernetes/ssl/admin-key.pem

# #set context parameters
# /opt/kubernetes/bin/kubectl config set-context kubernetes \
#   --cluster=kubernetes \
#   --user=admin

# #set default context
# /opt/kubernetes/bin/kubectl config use-context kubernetes
