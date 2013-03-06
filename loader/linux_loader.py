import sys,os
from subprocess import Popen
from server.tcpdns import TCPDNS
from server.udpdns import UDPDNS
from daemon import Daemon

def load(cfg):
    if os.geteuid() !=0:
        print '>> Please run this service as root.'
        os._exit(1)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            dns = TCPDNS(cfg) 
            dns.start()
        elif 'stop' == sys.argv[1]:
            dns = Daemon()
            dns.stop()
        elif 'restart' == sys.argv[1]:
            dns = TCPDNS(cfg) 
            dns.restart()
        elif 'censor' == sys.argv[1]:
            dns = UDPDNS(cfg)
            dns.start()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        dns = Daemon()
        tmp = dns.getstate()
        print "usage: %s start|stop|restart" % sys.argv[0]
        print "special usage: %s double-recv" % sys.argv[0]
        print '-------------------------------------'
        if tmp:
            print 'The daemon is running'
        else:
            print 'The daemon is stopped'
        sys.exit(2)
