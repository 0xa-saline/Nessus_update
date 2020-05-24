# Docker 下运行nessus

宿主机

```
docker run -ti -p 8834:8834 --name=nessus -v $(pwd):/tmp/nessus ubuntu:16.04
```
进入容器内修改源
```
mv /etc/apt/sources.list /etc/apt/sources.list_backup
vi /etc/apt/sources.list
deb-src http://archive.ubuntu.com/ubuntu xenial main restricted #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse #Added by software-properties
deb http://archive.canonical.com/ubuntu xenial partner
deb-src http://archive.canonical.com/ubuntu xenial partner
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse
```

```
apt-get update
apt-get install apt-utils libxdamage1 libgtk-3-0 libasound2 libnss3 libxss1 bzip2 wget net-tools expect libx11-xcb-dev dbus curl sudo net-tools vim openssh-server lrzsz inetutils-ping lsof tzdata -y
cd /tmp/nessus
dpkg -i Nessus-8.5.1-ubuntu1110_amd64.deb
```
访问Nessus安装服务


点继续 Managed by 选择 Tenable.sc

升级插件,可以在http://67.230.174.154/all-2.0.tar.gz下载

```
/etc/init.d/nessusd stop
/opt/nessus/sbin/nessuscli update /tmp/nessus/all-2.0.tar.gz
/etc/init.d/nessusd start
```

替换plugin_feed_info.inc的地方有两处
1. /opt/nessus/lib/nessus/plugins/目录下面的一个 (如果没有直接传一个上去)
2. /opt/nessus/lib/nessus/ 
```
cp /tmp/nessus/plugin_feed_info.inc /opt/nessus/lib/nessus/plugins/plugin_feed_info.inc
cp /tmp/nessus/plugin_feed_info.inc /opt/nessus/lib/nessus/plugin_feed_info.inc
```

回到宿主机
```
docker commit nessus nessus
# 获取images的id
docker ps -a  |grep nessus | grep ubuntu |awk '{print $1}'
# 进入容器
docker attach 5003e9c4865b
# 查看端口和进程，看看8834是否开启，进程nessus是否存在
ps aux |grep nessus
netstat -ntlp |grep 8834
# 如果没有的话就直接启动服务
/etc/init.d/nessusd start
```

修改密码

```
cd /opt/nessus/sbin/
./nessuscli -h
./nessuscli lsuser  列出用户
./nessuscli chpasswd user
```
