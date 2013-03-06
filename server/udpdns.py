'''
This module is still under development
Last updated: 2013-3-3
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
import select
from signal import SIGTERM, SIGQUIT,SIGINT,SIGKILL

from const import *
from server._base import *
from daemon import *

'''
This module provide a udp interceptor which can cencor all data received from dns server.
'''


class RequestHandlerToUDP(ThreadedDNSRequestHandler):


    '''
    Chech if the response contains fake ip
    Resolve the dns response according to rfc 1035
    '''
    def censor(self, data):
        rcode = (struct.unpack("!B", data[3])[0] & 15)
        aabit = (struct.unpack("!B", data[2])[0] & 4)
        if rcode != 0: # We only censor the successful response
            return True
        querycnt = struct.unpack("!H", data[4:6])[0]
        anscnt = struct.unpack("!H", data[6:8])[0]
        if anscnt == 0: return True
        anchor = 12
        for i in xrange(querycnt):
            anchor += domainlength(data[anchor:])
            anchor += 4
        for i in xrange(anscnt):
            namelen = 2
            if aabit:
                namelen = domainlength(data[anchor:])
            anchor += namelen
            tp = struct.unpack("!H", data[anchor : anchor + 2])[0]
            if tp != 1: # Only check type A response
                return True
            cls = struct.unpack("!H", data[anchor + 2 : anchor + 4])[0]
            if cls != 1: # Only check class IN response
                return True
            # Move forward anchor
            anchor += 10
            addr = '.'.join(str(j) for j in struct.unpack("!BBBB", data[anchor : anchor + 4]))
            print "[", addr, "]"
            if addr in fakeip: # Core!!
                return False
            anchor += 4
        return True


    '''
    still testing
    '''
    def queryremote(self, server, port, querydata):
        # RFC1035 section-4.2.2
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(3) # set socket timeout
            remote = (server, int(port))
            s.sendto(querydata, remote)
            expiration = time.time() + 60
            poll = select.poll()    
            poll.register(s.fileno(), select.POLLIN)
            #ret = poll.poll(1000000)
            while time.time() < expiration:
                # Wait read here
                pollret = poll.poll(60000)
                pollret = [i[0] for i in pollret]
                if s.fileno() in pollret:
                    (data, addr) = s.recvfrom(65535)
                    if addr[0] == server and self.censor(data):
                        return data
        except:
            print traceback.print_exc(sys.stdout)
            print "Trouble happened when using dns server: ", server
            if s: s.close()
            return
        if s: s.close()
        return data


class UDPDNS(Daemon):

    stopped = threading.Event()
    server = None

    def __init__(self, cfg):
        Daemon.__init__(self, '/tmp/test.pid', '/dev/null', 'stdout.log', 'stderr.log')
        self.dnscfg = cfg

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
        self.dnscfg.backup()
        self.dnscfg.modify('127.0.0.1')
        print '>> Please wait program init....'
        print '>> Init finished!'
        self.server = ThreadedUDPServer(('127.0.0.1', 53), RequestHandlerToUDP)
        self.server_thread = threading.Thread(target = self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        while self.run:
            time.sleep(1)
        self.server.shutdown()
        print '>> close server ,success'

    def terminate(self, signal, param):
        self.run = False
        self.force_close()
        self.dnscfg.restore()
        os._exit(0)

