#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
# parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$filePath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

#download ca files from master1 to local
# /bin/sh ${downloadFile} master1 ${remoteSslPath}/ca.csr ${filePath}
#check remote path
# fab -c ${fabFile} checkRemotePath --path "/opt/kubernetes/ssl" --nodename master1

# nodeName="node1"
# sedRegex="s/^--hostname-override={nodeName}/--hostname-override=${nodeName}/g"
# cat ${kbsConfigPath}/kube-kubelet.conf | sed "${sedRegex}" > ./tmp/test.conf
# cat ./tmp/test.conf
# ETCD_DATA_DIR="/"
# if [ -n "$ETCD_DATA_DIR" ] && [ -d "$ETCD_DATA_DIR" ] && [ "$ETCD_DATA_DIR" != "/" ]; then
#     echo "cache files of etcd is removed"
# fi

# domainName="sslexample.foo.com"
# secretName=$(echo ${domainName} | sed "s/\./\-/g")
# echo $secretName

fab -c ${fabFileCommon} download --dirremote "/opt/kubernetes/ssl/kubernetes.pem" --dirlocal "${rootPath}/tmp/" --nodename master1