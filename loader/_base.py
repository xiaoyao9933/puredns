import platform

def create_loader():
    s = platform.system()
    if s == "Darwin":
        from loader.linux_loader import load
        return load
    elif s == "Linux":
        from loader.linux_loader import load
        return load
    elif s == "Windows":
        from loader.windows_loader import load
        return load
    else:
        print "Unsuppoerted os"
        
