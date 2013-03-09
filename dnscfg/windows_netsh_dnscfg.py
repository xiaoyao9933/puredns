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
    def __init__(self):
        self.backupfile = os.path.expanduser('~') + os.path.sep + 'puredns_backup.log'
        self.backup_data = {}
        self.notadmin = not self.backup()
        
    def backup(self):
        backup_file = None
        # check for previous saved backup
        try:
            backup_file = open(self.backupfile, 'r')
            print '>> Not normally closed last time, will set dns to backup.'
            self.backup_data = eval(backup_file.read())
            return True
        except:
            pass
        finally:
            if backup_file != None:
                backup_file.close()
                backup_file = None
        # get the current primary dns settings fro all connected interfaces and make backup
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
            self.backup_data = result
            backup_file = open(self.backupfile, 'w')
            backup_data_json = repr(self.backup_data)
            backup_file.write(backup_data_json)
            return True
        except:
            print 'failed to backup'
            return False
        finally:
            if backup_file != None:
                backup_file.close()

    def modify(self, dns):
        cmd = ['pushd interface ip']
        for interface in self.backup_data.keys():
            cmd.append('set dns "' + interface + '" source=static addr=' + dns + ' register=PRIMARY')
        cmd.append('popd\n')
        process = subprocess.Popen('netsh', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.communicate('\n'.join(cmd))

    def restore(self):
        cmd = ['pushd interface ip']
        for interface in self.backup_data.keys():
            if self.backup_data[interface] == 'auto':
                cmd.append('set dns "' + interface + '" source=dhcp register=PRIMARY')
            else:
                cmd.append('set dns "' + interface + '" source=static addr=' + self.backup_data[interface] + ' register=PRIMARY')
        cmd.append('popd\n')
        process = subprocess.Popen('netsh', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.communicate('\n'.join(cmd))
        try:
            os.unlink(self.backupfile)
        except:
            pass    # just ignore if the backup file doesn't exist

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
