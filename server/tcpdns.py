#! /usr/bin/python
# -*- coding: utf-8 -*-
# cody by zhouzhenster@gmail.com modified by xiaoyao9933(me@chao.lu)

# ver: 0.2 update 2011-10-23
#           use SocketServer to run a multithread udp server
# update:
# 2012-04-16, add more public dns servers support tcp dns query
#  8.8.8.8        google
#  8.8.4.4        google
#  156.154.70.1   Dnsadvantage
#  156.154.71.1   Dnsadvantage
#  208.67.222.222 OpenDNS
#  208.67.220.220 OpenDNS
#  198.153.192.1  Norton
#  198.153.194.1  Norton
'''
Last updated: 2013-3-1
By: Ming
Email: mjzshd@gmail.com
'''
import os, sys
import socket
import struct
import threading
import SocketServer
import traceback
import random
from signal import SIGTERM, SIGQUIT,SIGINT,SIGKILL

from const import *
from server._base import *
from daemon import *


class RequestHandlerToTCP(ThreadedDNSRequestHandler):

    '''
    query remote tcp server
    follow rfc1035
    '''
    def queryremote(self, server, port, querydata):
        # RFC1035 section-4.2.2
        print "qurey! server: ", server
        Buflen = struct.pack('!h', len(querydata))
        sendbuf = Buflen + querydata
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT) # set socket timeout
            s.connect((server, int(port)))
            s.send(sendbuf)
            data = s.recv(2048)
        except:
            print traceback.print_exc(sys.stdout)
            if s: s.close()
            return
        if s: s.close()
        return data


class TCPDNS(Daemon):

    stopped = threading.Event()
    server = None

    def __init__(self, cfg):
        Daemon.__init__(self, '/tmp/test.pid', '/dev/null', 'stdout.log', 'stderr.log')
        self.dnscfg = cfg
        
    def serve_forever(self):
        while not self.stopped.is_set():
            try:
                self.server.handle_request()
            except:
			    pass
        self.server.socket.close()
        #self._Thread__stop()

    def force_close(self):
        self.stopped.set()
        #FIXME: What the dummy request for?
        self.create_dummy_request()
        
    def create_dummy_request(self):
        address = ('127.0.0.1', 53)
        sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockudp.sendto('fake data fake datafake datafake datafake datafake datafake datafake data',address)
        print '>> Send dummy'
	
    def run(self):
        self.run = True
        signal.signal(signal.SIGQUIT, self.terminate)
        #signal.signal(signal.SIGKILL, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        signal.signal(signal.SIGTERM, self.terminate)
        self.dnscfg.backup()
        self.dnscfg.modify('127.0.0.1')
        print '>> Please wait program init....'
        print '>> Init finished!'
        self.server = ThreadedUDPServer(('127.0.0.1', 53), RequestHandlerToTCP)
        self.server_thread = threading.Thread(target = self.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        while self.run:
            time.sleep(1)
        print '>> close server ,success'

    def terminate(self, signal, param):
        self.run = False
        self.force_close()
        self.dnscfg.restore()
        os._exit(0)

