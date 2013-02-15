# -*- coding: utf-8 -*-
# FileName: PureDNSDeamon.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-02-15
# Vesion  : 1.0
import sys, os, time, atexit, signal
import DNSCfg_Linux as DNSCfg
import threading
import tcpdns
from subprocess import Popen
from signal import SIGTERM, SIGQUIT,SIGINT,SIGKILL

class Daemon:
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin = '/dev/null', stdout = '/dev/null', stderr = '/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
       # os.chdir("~/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'w')
        se = file(self.stderr, 'w', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)
    def getstate(self):
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if pid:
            return True
        else:
            return False
    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "Daemon is already running\n"
            sys.stderr.write(message)
            sys.exit(1)

        # Start the daemon
        sys.stdout.write('Start Success\n')
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "Daemon is not running\n"
            sys.stderr.write(message)
            return # not an error in a restart
        # Try killing the daemon process    
        try:
            while True:
                os.kill(pid, SIGQUIT)
                sys.stdout.write('Stop Success\n')
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)
    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()
    def run(self):
        self.run = True
        signal.signal(signal.SIGQUIT, self.terminate)
        #signal.signal(signal.SIGKILL, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        signal.signal(signal.SIGTERM, self.terminate)
        self.dnscfg=DNSCfg.DNSCfg()
        self.tcpdns=tcpdns.tcpdns()
        self.dnscfg.ModifyDns('127.0.0.1')
        while self.run:
            time.sleep(1)
    def terminate(self, signal, param):
        self.run = False
        self.tcpdns.force_close()
        self.dnscfg.RestoreDns()
        os._exit(0)

