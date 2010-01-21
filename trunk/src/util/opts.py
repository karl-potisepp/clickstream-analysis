'''
Created on 21.01.2010

@author: Riivo
'''
import getopt, os, sys
import config

def read_opts(argv):
    logfile = None
    filelist = config.paths
    support = config.support    
    try:
        opts, args = getopt.getopt(argv, 's:', ["support"])
        if len(args) == 1:
            logfile = args[0]
        
        support = config.support
        for o, a in opts:
            if o in ("-s", "--support"):
                if a.find(".")!=-1:
                    support = float(a)
                    if support > 1.0: raise getopt.GetoptError("support cannot be bigger than 1.0") 
                else:
                    support = int(a)
            else:
                raise getopt.GetoptError("incompatible arguments")


    except getopt.GetoptError, err:
        print "Error: " + str(err)
        sys.exit(2)    
    
    if logfile is not None:
        if os.path.isdir(logfile) :
            filelist = map(lambda x: os.path.join(logfile, x), os.listdir(logfile))
            filelist = filter(lambda x: os.path.isfile(x), filelist)
        else:
            filelist = [logfile]
    
    return filelist, support