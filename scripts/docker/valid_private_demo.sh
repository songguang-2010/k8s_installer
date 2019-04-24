#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh

fab -c ${fabFile} validDemoDockerPrivate

# exit 0

# load config items
# . ${configPath}/config_var.sh

# #get docker secret
# cmdRemote="${remoteBinPath}/kubectl get secret"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #valid
# imageId=$(docker images | grep registry.cn-beijing.aliyuncs.com/ducafe/busybox | awk '{print $3}')

# if [ -z $imageId ]; then
#     docker pull registry.cn-beijing.aliyuncs.com/ducafe/busybox:1.24
#     imageId=$(docker images | grep registry.cn-beijing.aliyuncs.com/ducafe/busybox | awk '{print $3}')
#     #login docker registry
#     docker login --username=${DOCKER_USERNAME} ${DOCKER_DOMAIN} --password=${DOCKER_PASSWORD}

#     docker tag ${imageId} ${DOCKER_DOMAIN}/kube-systems/busybox-demo:1.24
#     docker images
#     docker push ${DOCKER_DOMAIN}/kube-systems/busybox-demo:1.24
# fi


# #uninstall old service
# cmdRemote="${remoteBinPath}/kubectl delete -f ${remotePluginPath}/docker/busybox-demo.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# #upload
# /bin/sh ${uploadFile} master1 ${filePath}/busybox-demo.yaml ${remotePluginPath}/docker/
# #install
# cmdRemote="${remoteBinPath}/kubectl create -f ${remotePluginPath}/docker/busybox-demo.yaml"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1

# sleep 5s

# #view
# cmdRemote="${remoteBinPath}/kubectl get pods busybox-demo"
# fab -c ${fabFile} sudo --cmd "${cmdRemote}" --nodename master1


