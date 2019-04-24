#!/bin/sh

#app root directory
# rootPath=$(cd "$(dirname "$parent")"; pwd)
#temp directory
tmpPath="${rootPath}/tmp"
#scripts directory
scriptsPath="${rootPath}/scripts"
#app resource path
resourcePath="${rootPath}/resource"
#app config path
configPath="${rootPath}/config"

#kbs binary file path
kbsBinPath="${resourcePath}/kubernetes/server/bin"
#flannel binary file path
flannelBinPath="${resourcePath}/flannel"
#weave binary file path
weaveBinPath="${resourcePath}/weave"
#cni binary file path
cniBinPath="${resourcePath}/cni"
#cfssl binary file path
cfsslBinPath="${resourcePath}/cfssl"
#etcd binary file path
etcdBinPath="${resourcePath}/etcd"
#etcd config path
etcdConfigPath="${configPath}/etcd"
#kbs config path
kbsConfigPath="${configPath}/kbs"
#flannel config path
flannelConfigPath="${configPath}/flannel"
#cni config path
cniConfigPath="${configPath}/cni"

#fab file to invoke to run some task
fabFile="${scriptsPath}/common/fabfile"
fabFileCommon="${scriptsPath}/common/fabfile_common"
#upload file to invoke to upload local file to remote
uploadFile="${scriptsPath}/common/upload_file.sh"
#upload file to invoke to upload local file to remote
downloadFile="${scriptsPath}/common/download_file.sh"
#exec file to invoke to excute remote file in remote server
execFile="${scriptsPath}/common/exec_file.sh"

#remote parameters
remoteKbsPath="/opt/kubernetes"
remoteSslPath="${remoteKbsPath}/ssl"
remoteCfgPath="${remoteKbsPath}/cfg"
remoteBinPath="${remoteKbsPath}/bin"
remoteLocalBinPath="/usr/local/bin"
remoteCniBinPath="/opt/cni/bin"
remoteCniCfgPath="/etc/cni/net.d"
remotePluginPath="${remoteKbsPath}/addons"
remoteDemoPath="${remoteKbsPath}/demo"
remoteSystemdPath="/usr/lib/systemd/system"
remoteTmpPath="/tmp"