# 欢迎使用PureDNS 

## 什么是PureDNS?

众所周知，由于某种原因封锁了对一些境外网站如youtube,twitter,facebook的访问。但总结起来，其主要的三个技术：

*    链接重置
*    DNS污染
*    路由黑洞

其中对主流网站采取的多是前两种方法。但由于关键词过滤的原因，其对Https的检测往往不奏效，导致连接重置不起作用。这时我们只要获取到了网站的正确ip，就依然可以通过https连接到这个网站。 普通的境外DNS查询会受到关键词过滤，而被DNS污染，但由于目前其对TCP和两次接收UDP连接的DNS查询不设防，本工具就利用此特性制作了一个本地DNS代理服务器，TCP访问8.8.8.8等，并自动的将DNS设置为127.0.0.1。 所以本工具的适用网站范围：

*   在开启本代理后可以ping通
*    开启了Https连接

已知可以访问的网站：

*    [https://www.youtube.com](https://www.youtube.com)(youtube视频打不开的原因，原来是视频源是通过http传输的，这个过几天可能就好了)
*    [https://www.facebook.com](https://www.facebook.com)(完美支持)
*    [https://www.twitter.com](https://www.twitter.com)（因地方而异，有的地方路由黑洞了，我这里没问题）
    等等 

## 你将获得什么？
* 不再饱受DNS被劫持之苦（比如乱插广告）
* 不再担心DNS污染的方式中间人攻击
* 上某些网站
* 不用再去改hosts表，那么低端的方法了
* 网速比较快

## 使用方法
不管你使用那个操作系统，如果你之前改过hosts表，请清空与被禁网站相关的表项。hosts原有表项会破坏dns的解析。
最好使用Firefox或者chrome浏览器，并安装这个插件[HTTPS Everywhere](https://www.eff.org/https-everywhere)，它可以自动帮助你连接支持https的网站。里面支持https的列表相当多。

### Windows
双击运行本软件即可，通知栏会产生一个服务图标，用户可以在这里控制。打开被封杀的网页时一定要加上https:// ,如 https://www.youtube.com
### Linux/Mac

使用方法：

*    先从下面下载PureDNS.tar.gz ,解压缩到一个目录，确保你已经安装python2.6+
*    打开一个终端，执行:sudo python PureDNS.py start
*    由于写成了服务，关掉终端也可以了，如果想终止该服务，请输入 sudo python PureDNS.py stop
*    如果想启动利用两次接收UDP的方法，可以运行sudo python PureDNS.py censor 
就这样吧，我就不去打包了。

## FAQ
*    Q：本工具长期有效么？ A： 理论上是这样，但是由于路由黑洞的不确定性，可能存在上不去某些网站的情况。但本法成功率绝对比改Hosts高。
*    Q：本工具是不是网速很慢？ A：不会的，由于DNS查询只是解析时起作用，实际观看youtube视频等，流量是不经第三方中转的，从这个角度说，本工具技术上合法。
*    Q：极特殊情况下，比如异常关机，强行杀死程序，退出软件后无法打开网页？ A：重新启动本软件一次即可自动修复。
*    Q: 如何分享给其他机子使用，如果不同机子的ip可以互相访问，你可以在其他机子上的DNS设置为运行PureDNS的ip地址，这样就可以使你的ipad等分享该DNS。
*    Q: 有人说我弄麻烦了，用udp的两次recv就可以。 A：嗯，是这样的，我刚开始做这个时候脑袋短路了，等这个不能用了的时候再用二次recv吧
*    Q：本工具其实只是防止DNS污染的一个小工具，只是作为改Hosts表的一种良好的替代方案。
*    Q: 用了本代理后google打不开了，怎么办？ A：墙对google看起来是特殊关照了，你还是老老实实的访问g.cn吧，如果你使用了HTTPS Everywhere，先进g.cn，点击地址栏的插件图标，取消掉 google search的选项，以后就用g.cn吧。
## 其他信息
*  

* 作者博客：[chao.lu](http://chao.lu)
* Github上的[源代码](https://github.com/xiaoyao9933/puredns)
* 最新windows版[下载](https://sourceforge.net/projects/puredns/files/PureDNS.exe/download)
* 最新Linux/Mac版[下载](https://sourceforge.net/projects/puredns/files/PureDNS.tar.gz/download)

## Update Logs：
*   1.3 : 感谢在mjzshd(mjzshd@gmail.com)的帮助下，重构了我的代码，改正了代码很多的Bugs，增加了MAC版本，添加了两次接收UDP的censor法，让本渣学到了很多新知识。
*   1.2 : 不改版本号了，增加了非管理员权限执行时的提示信息。
*   1.2 : 修复了没关闭软件时，直接关闭系统导致dns设置不能还原的BUG。增加了异常退出的自动修复机制。
*   1.1 : 修复了有些情况退出后，不能还原DNS设置，以致不能打开网页的问题。增加了错误报告的捕获。
