import sys,os
from subprocess import Popen
from tcpdns import TCPDNS

def load(cfg):
    if os.geteuid() !=0:
        print '>> Please run this service as root.'
        os._exit(1)
    dns = TCPDNS(cfg) 
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            dns.start()
        elif 'stop' == sys.argv[1]:
            dns.stop()
        elif 'restart' == sys.argv[1]:
            dns.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        tmp = dns.getstate()
        print "usage: %s start|stop|restart" % sys.argv[0]
        print '-------------------------------------'
        if tmp:
            print 'The daemon is running'
        else:
            print 'The daemon is stopped'
        sys.exit(2)
