该项目是安装kubernetes集群的完整脚本集合，该项目中采用了k8s+coredns+flannel+etcd的集成方案。

环境依赖：
centos7.6
python v3.5+
python-pip v19.0.3
python packages: fabric v2.0, patchwork v1.0.1, invocations v1.4.0

软件版本：
kubernetes release: v1.13.3
etcd release: v3.3.12
docker release: docker-ce-cli-18.06.3
cfssl: 1.2.0
weave release: v2.5.1
cni plugins: v0.7.4
metrics-server release: v0.3.1

硬性要求：
最少四个节点，3个master节点，一个worker节点

