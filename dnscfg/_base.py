import platform

class DNSCfg(object):

    def __init__(self):
        pass

    def backup(self):
        pass

    def modify(self, dns):
        pass

    def restore(self):
        pass

    def printinfo(self):
        pass


def create_dnscfg():
    s = platform.system()
    if s == "Darwin":
        from dnscfg.darwin_dnscfg import DarwinDNSCfg
        return DarwinDNSCfg()
    elif s == "Linux":
        from dnscfg.linux_dnscfg import LinuxDNSCfg
        return LinuxDNSCfg()
    elif s == "Windows":
        try:
            from dnscfg.windows_dnscfg import WindowsDNSCfg
            return WindowsDNSCfg()
        except:
            print 'wmi method not working try netsh'
            from dnscfg.windows_netsh_dnscfg import WindowsNetshDNSCfg
            return WindowsNetshDNSCfg()
    else:
        print "Unsuppoerted os"
        
