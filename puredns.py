import dnscfg
import loader

if __name__ == "__main__":

    cfg = dnscfg.create_dnscfg()
    load = loader.create_loader()
    
    # Start loading app
    load(cfg)
