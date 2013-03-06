#! /usr/bin/python
# -*- coding: utf-8 -*-
# FileName: windows_netsh_dnscfg.py
# Author  : davidaq
# Email   : aq@num16.com
# Date    : 2013-03-07
from dnscfg import DNSCfg
import os
import subprocess
import re
########################################################################
class WindowsNetshDNSCfg(DNSCfg):
    def backup(self):
        file = None
        try:
            raw_result = subprocess.check_output('netsh interface ip show dns')
            ip = re.compile(r'\d+\.\d+\.\d+\.\d+')
            result = {}
            for interface in self.interfaces():
                pos = raw_result.find('"' + interface + '"')
                pos = raw_result.find('\n', pos) + 1
                end = raw_result.find('\n', pos)
                line = raw_result[pos:end]
                result[interface] = 'auto'
                if 'DHCP' not in line and 'dhcp' not in line:
                    match = ip.search(line)
                    if match != None:
                        result[interface] = match.group()
            file = open(self.backupfile(), 'w')
            file.write(repr(result))
        except:
            print 'failed to backup'
            return True
        finally:
            if file != None:
                file.close()
    
    def modify(self, dns):
        cmd = ['pushd interface ip']
        for interface in self.interfaces():
            cmd.append('set dns "' + interface + '" source=static addr=' + dns + ' register=PRIMARY')
        cmd.append('popd\n')
        process = subprocess.Popen('netsh', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.communicate('\n'.join(cmd))

    def restore(self):
        file = None
        try:
            file = open(self.backupfile(), 'r')
            backup = file.read()
        except:
            return True
        backup = eval(backup)
        cmd = ['pushd interface ip']
        for interface in backup.keys():
            if backup[interface] == 'auto':
                cmd.append('set dns "' + interface + '" source=dhcp register=PRIMARY')
            else:
                cmd.append('set dns "' + interface + '" source=static addr=' + backup[interface] + ' register=PRIMARY')
        cmd.append('popd\n')
        process = subprocess.Popen('netsh', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.communicate('\n'.join(cmd))
    
    def backupfile(self):
        return os.path.expanduser('~') + os.path.sep + 'puredns_backup.log'
        
    def interfaces(self):
        raw_result = subprocess.check_output('netsh interface ip show interfaces')
        result = []
        token = ' connected'
        for line in raw_result.split('\n'):
            pos = line.find(token)
            if pos > -1:
                item = line[pos + len(token):].strip()
                result.append(item)
        return result
        
def printinfo():
    print 'None'
