#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#parent directory
parentPath=$(cd "$(dirname "$filePath")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$parentPath")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

fab -c ${fabFile} --pty installKbsMasterBefore
fab -c ${fabFile} --pty installKbsMasterNormal --nodename master1
fab -c ${fabFile} --pty installKbsMasterNormal --nodename master2
fab -c ${fabFile} --pty installKbsMasterNormal --nodename master3
# fab -c ${fabFile} --pty installKbsMasterAfter

