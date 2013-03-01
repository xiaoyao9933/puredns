# -*- coding: utf-8 -*-
# FileName: DNSCfg.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-02-14
# Vesion  : 1.2
import os

class LinuxDNSCfg(DNSCfg):
    def __init__(self):
        self.backup()
    #----------------------------------------------------------------------
    # Get the Adapter who has mac from wmi 
    #----------------------------------------------------------------------
    def backup(self):
        try:
            dnsfile = open('/etc/resolv.conf','r+')
            backupfile = open('/etc/puredns.conf','w+')
            self.backup = backupfile.read()
            self.conf = dnsfile.read()
            dnsfile.seek(0)
            backupfile.seek(0)
            if '127.0.0.1' in self.conf: # When resolv.conf file already be modified
                if 'nameserver' in self.backup: # backup file is fine
                    dnsfile.write(self.backup)
                else: # backupfile got lost
                    backupfile.writelines(['nameserver 8.8.8.8\n','nameserver 8.8.8.4\n'])
            else:
                backupfile.write(self.conf)
        except:
            print 'fileread error'
        finally:
            dnsfile.close()
            backupfile.close()
    #----------------------------------------------------------------------
    # Modify DNS
    #----------------------------------------------------------------------
    def  modify(self,dns):
        try:
            dnsfile = open('/etc/resolv.conf','w')
            dnsfile.writelines(['nameserver '+dns+'\n'])
            print '>> Modified'
        finally:
            dnsfile.close()
    #----------------------------------------------------------------------
    # Restore DNS
    #----------------------------------------------------------------------
    def restore(self):
        try:
            dnsfile = open('/etc/resolv.conf','w')
            backupfile = open('/etc/puredns.conf','r')
            self.backup = backupfile.read()
            dnsfile.write(self.backup)
            print '>> Restored!'
        finally:
            dnsfile.close()
            backupfile.close()
def printinfo():
    print 'None'
