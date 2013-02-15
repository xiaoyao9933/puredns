# -*- coding: utf-8 -*-
# FileName: DNSCfg.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-02-14
# Vesion  : 1.2
import os

class DNSCfg:
    def __init__(self):
        self.GetDNSBackup()
    #----------------------------------------------------------------------
    # Get the Adapter who has mac from wmi 
    #----------------------------------------------------------------------
    def GetDNSBackup(self):
        try:
            dnsfile = open('/etc/resolv.conf','r+')
            backupfile = open('/etc/puredns.conf','r+')
            self.backup = backupfile.read()
            self.conf = dnsfile.read()
            dnsfile.seek(0)
            backupfile.seek(0)
            if '127.0.0.1' in self.conf:
                if 'nameserver' in self.backup:
                    dnsfile.write(self.backup)
                else:
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
    def  ModifyDns(self,dns):
        try:
            dnsfile = open('/etc/resolv.conf','w')
            dnsfile.writelines(['nameserver '+dns+'\n'])
            print '>> Modified'
        finally:
            dnsfile.close()
    #----------------------------------------------------------------------
    # Restore DNS
    #----------------------------------------------------------------------
    def RestoreDns(self):
        try:
            dnsfile = open('/etc/resolv.conf','w')
            backupfile = open('/etc/puredns.conf','r')
            self.backup = backupfile.read()
            dnsfile.write(self.backup)
            print '>> Restored!'
        finally:
            dnsfile.close()
            backupfile.close()
def PrintInfo():
    print 'None'
