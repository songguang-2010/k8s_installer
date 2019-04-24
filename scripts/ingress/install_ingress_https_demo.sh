#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} installDemoIngressHttps

# load config items
# . ${configPath}/config_var.sh

# # tls support
# domainName="sslexample.foo.com"
# secretName=$(echo ${domainName} | sed "s/\./\-/g")

# echo "generate tls key file ..."
# keyFile="${remoteSslPath}/tls-ingress-example.key"
# certFile="${remoteSslPath}/tls-ingress-example.crt"
# #generate tls key
# cmdRemote="openssl genrsa -out /opt/kubernetes/ssl/tls-ingress-example.key 2048"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #generate tls cert
# echo "generate tls cert file ..."
# cmdRemote="openssl req -new -x509 -key ${keyFile} -out ${certFile}"
# cmdRemote="${cmdRemote} -subj /C=CN/ST=Beijing/L=Beijing/O=DevOps/CN=${domainName}"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #generate secret
# echo "generate secret ..."
# cmdRemote="${remoteBinPath}/kubectl create secret tls ${secretName} --cert=${certFile} --key=${keyFile}"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #get secret
# echo "get secret ..."
# cmdRemote="${remoteBinPath}/kubectl get secret"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #describe secret
# echo "describe secret ..."
# cmdRemote="${remoteBinPath}/kubectl describe secret ${secretName}"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# # remove ingress rules of https
# echo "remove ingress rules of https ..."
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/ingress/nginx-ingress-rules-https.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
# #upload ingress rules of https
# echo "upload ingress rules yaml ..."
# /bin/sh ${uploadFile} master1 ${filePath}/nginx-ingress-rules-https.yaml ${remotePluginPath}/ingress/
# #install ingress rules of https
# echo "install ingress rules ..."
# cmdRemote="${remoteBinPath}/kubectl apply -f ${remotePluginPath}/ingress/nginx-ingress-rules-https.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1