from linux_dnscfg import LinuxDNSCfg

class DarwinDNSCfg(LinuxDNSCfg):


    def backup(self):
        LinuxDNSCfg.backup(self)

    def modify(self, dns):
        LinuxDNSCfg.modify(self, dns)

    def restore(self):
        LinuxDNSCfg.restore(self)

    def printinfo(self):
        LinuxDNSCfg.printinfo(self)
