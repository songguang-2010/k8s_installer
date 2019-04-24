#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} installDockerPrivate

# load config items
# . ${configPath}/config_var.sh

# #login docker registry
# cmdRemote="docker login --username=${DOCKER_USERNAME} ${DOCKER_DOMAIN} --password=${DOCKER_PASSWORD}"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #download docker login config file form master1 to local
# /bin/sh ${downloadFile} master1 /root/.docker/config.json ${filePath}

# #view docker login config file content in local, and generate login credentials
# # cat ./config.json
# dockerSecret=$(cat ./config.json | base64 -w 0)
# sedRegex="s/{dockerSecret}/${dockerSecret}/g"
# cat ${filePath}/registry-pull-secret.yaml | sed "${sedRegex}" > ${tmpPath}/registry-pull-secret.yaml
# /bin/sh ${uploadFile} master1 ${tmpPath}/registry-pull-secret.yaml ${remoteCfgPath}/

#create docker secret pod
# cmdRemote="${remoteBinPath}/kubectl create -f ${remoteCfgPath}/registry-pull-secret.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

#get docker secret
# cmdRemote="${remoteBinPath}/kubectl get secret"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1
