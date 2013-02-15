#! /usr/bin/python
# -*- coding: utf-8 -*-
# FileName: PureDNS.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-02-15
# Vesion  : 1.0
#!/usr/bin/env python  
import sys,os
from PureDNSDeamon import Daemon
from subprocess import Popen
           # time.sleep(1)
if __name__ == "__main__":
    if os.geteuid() !=0:
        print '>> Please run this service as root.'
        os._exit(1)
    daemon = Daemon('/tmp/test.pid', '/dev/null', 'stdout.log', 'stderr.log')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        tmp = daemon.getstate()
        print "usage: %s start|stop|restart" % sys.argv[0]
        print '-------------------------------------'
        if tmp:
            print 'The daemon is running'
        else:
            print 'The daemon is stopped'
        sys.exit(2)
