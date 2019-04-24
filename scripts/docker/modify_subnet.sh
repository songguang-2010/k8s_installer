# service docker stop
# # 删除docker防火墙过滤规则
# iptables -t nat -F POSTROUTING
# # 删除docker默认网关配置
# ip link set dev docker0 down
# ip addr del 172.17.0.1/16 dev docker0
# # 增加新的docker网关配置
# ip addr add 9.2.0.1/24 dev docker0
# ip link set dev docker0 up
# # 检测是否配置成功，如果输出信息中有 192.168.5.1，则表明成功
# ip addr show docker0
# service docker start
# # 验证docker防火墙过滤规则

ExecStart=/usr/bin/dockerd --bip=9.2.0.1/24
