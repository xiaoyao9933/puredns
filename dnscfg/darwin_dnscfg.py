from linux_dnscfg import LinuxDNSCfg
import json
import os
import subprocess

class DarwinDNSCfg(LinuxDNSCfg):


    def backup(self):
        '''
            Didn't consider the case when some other force remove the backupfile
        '''
        LinuxDNSCfg.backup(self)
        backupfile = None
        if 'puredns_darwin.conf' in os.listdir("/etc"):
            return
        try:
            backupfile = open('/etc/puredns_darwin.conf', 'w+')
            conf = {}
            services = self.getallnetworkservices()
            
            for service in services:
                servers = self.getdnsservers(service)
                conf[service] = servers

            jsonconf = json.dumps(conf)
            backupfile.write(jsonconf)
        except Exception as e:
            print e
        finally:
            if backupfile: backupfile.close()
               

    def modify(self, dns):
        LinuxDNSCfg.modify(self, dns)
        services = self.getallnetworkservices()
        for service in services:
            self.setdnsservers(service, [dns])

    def restore(self):
        LinuxDNSCfg.restore(self)
        backupfile = None
        backupfilelocation = "/etc/puredns_darwin.conf"
        try: 
            backupfile = open(backupfilelocation, "r")
            backup = backupfile.read()
            conf = json.loads(backup)
            for key in conf:
                self.setdnsservers(key, conf[key])
        finally:
            if backupfile:
                backupfile.close()
                os.remove(backupfilelocation)

    def printinfo(self):
        pass

    def getallnetworkservices(self):
        try: 
            ret = subprocess.check_output(["networksetup", "-listallnetworkservices"])
            ret = ret.split("\n")
            ret.remove('')
            ret.remove('An asterisk (*) denotes that a network service is disabled.')
            return ret
        except subprocess.CalledProcessError as e:
            print "getallnetworkservices failed: ", e
        return []

    def getdnsservers(self, service):
        try:
            ret = subprocess.check_output(["networksetup", "-getdnsservers", service])
            ret = ret.split("\n")
            ret.remove('')
            if len(ret) > 0 and "There aren't any " in ret[0]:
                return []
            return ret
        except subprocess.CalledProcessError as e:
            print "getdnsservers failed: ", e
        return ret

    def setdnsservers(self, service, dnsservers):
        try:
            init = ["networksetup", "-setdnsservers", service] + dnsservers
            ret = subprocess.check_output(init)
        except subprocess.CalledProcessError as e:
            print "setdnsservers failed: ", e


    
