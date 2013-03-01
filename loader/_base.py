import platform
def create_loader():
    s = platform.system()
    if s == "Darwin":
        from loader.linux_loader import loader
        return loader
    else if s == "Linux":
        from loader.linux_loader import loader
        return loader
    else if s == "Windows":
        from loader.windows_loader import loader
        return loader
    else:
        print "Unsuppoerted os"
        
