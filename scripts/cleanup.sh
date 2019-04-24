#!/bin/sh

#当前文件所在路径
filePath=$(cd "$(dirname "$0")"; pwd)
#root directory
rootPath=$(cd "$(dirname "$filePath")"; pwd)

. ${rootPath}/scripts/common/constant.sh
# load config items
# . ${configPath}/config_var.sh

fab -c ${fabFile} --pty cleanupComponents

fab -c ${fabFile} --pty cleanupFiles --nodename node2
fab -c ${fabFile} --pty cleanupFiles --nodename node1
fab -c ${fabFile} --pty cleanupFiles --nodename master1
fab -c ${fabFile} --pty cleanupFiles --nodename master2
fab -c ${fabFile} --pty cleanupFiles --nodename master3
