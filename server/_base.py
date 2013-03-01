import os, sys
import socket
import struct
import threading
import SocketServer
import traceback
import random

#-------------------------------------------------------------
# Hexdump Cool :)
# default width 16
#--------------------------------------------------------------
def hexdump( src, width=16 ):
    FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
    result=[]
    for i in xrange(0, len(src), width):
        s = src[i:i+width]
        hexa = ' '.join(["%02X"%ord(x) for x in s])
        printable = s.translate(FILTER)
        result.append("%04X   %s   %s\n" % (i, hexa, printable))
    return ''.join(result)


#---------------------------------------------------------------
# bytetodomain
# 03www06google02cn00 => www.google.cn
#--------------------------------------------------------------
def bytetodomain(s):
    domain = ''
    i = 0
    length = struct.unpack('!B', s[0:1])[0]
  
    while length != 0 :
        i += 1
        domain += s[i:i+length]
        i += length
        length = struct.unpack('!B', s[i:i+1])[0]
        if length != 0 :
            domain += '.'
  
    return domain

def resolve_request(data):
    domain = bytetodomain(querydata[12:-4])
    qtype = struct.unpack('!h', querydata[-4:-2])[0]
    return (domain, qtype)


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    def __init__(self, s, t):
        SocketServer.UDPServer.__init__(self, s, t)


def ThreadedDNSRequestHandler(SocketServer.BaseRequestHandler):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    #-----------------------------------------------------
    # send udp dns respones back to client program
    #----------------------------------------------------
    def transfer(self, addr, server):
        if not querydata: return

        (domain, qtype) = resolve_request(data)
        """
        print 'domain:%s, qtype:%x, thread:%d' % \
             (domain, qtype, threading.activeCount())
        """
        sys.stdout.flush()
        choose = random.sample(xrange(len(DHOSTS)), 1)[0]
        DHOST = DHOSTS[choose]
        response = self.queryremote(DHOST, DPORT, querydata)
        if response:
            # udp dns packet no length
            server.sendto(response[2:], addr)

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        addr = self.client_address
        try:
            self.transfer(data, addr, socket)
        except:
            pass
