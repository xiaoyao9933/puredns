class DarwinDNSCfg(LinuxDNSCfg):


    def __init__(self):
        LinuxDNSCfg.__init__(self)
        self.backup()
    
    def backup(self):
        pass

    def modify(self, dns):
        pass

    def restore(self):
        pass

    def printinfo(self):
        pass
