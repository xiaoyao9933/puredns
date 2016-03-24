# PureDNS 

简单的DNS无污染代理。

## 使用方法

### Windows

双击运行本软件即可，通知栏会产生一个服务图标，用户可以在这里控制。
### Linux/Mac

使用方法：

*    先从下面下载PureDNS.tar.gz ,解压缩到一个目录，确保你已经安装python2.6+
*    打开一个终端，执行:sudo python PureDNS.py start
*    由于写成了服务，关掉终端也可以了，如果想终止该服务，请输入 sudo python PureDNS.py stop
*    如果想启动利用两次接收UDP的方法，可以运行sudo python PureDNS.py censor 
