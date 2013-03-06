from dnscfg import DNSCfg

class WindowsNetshDNSCfg(DNSCfg):
    def backup(self):
        pass
    
    def modify(self, dns):
        print dns

    def restore(self):
        pass
    
def printinfo():
    print 'None'
