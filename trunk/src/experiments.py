import sys, getopt, os

import apachelogs, logparser
import fsm_wrapper
import time_decorator
import config
import apriori


def analyse_clickstream(paths, support):

    # read log files
    log = apachelogs.ApacheLogFile(*paths)

    # parse log files, extract sessions
    parser = logparser.LogParser(log, [])
    parser.parse()
    
    
    transactions = [session for session in parser.get_simple_sessions() if config.filter_fn(session)]
    n = len(transactions)

    support = 0.9
    x = []
    y = []
    while support >= 0.001:
      
        min_support = int(len(transactions) * support)
        #results = fsm_wrapper.fpm(transactions, min_support)
        results = apriori.extract_itemsets(transactions, min_support)
        print support,";",len(results)
        
        x.append(len(results))
        y.append(support)
        support = support - 0.01
    
    import pylab
    pylab.figure(figsize=(8, 4))
    pylab.plot(y, x)

    ax = pylab.axes()
    ax.set_xlim(min(y), max(y))
    #ax.xaxis.set_major_formatter(majorFormatter)
    #ax.xaxis.set_major_locator(maxlocator)
    ax.set_xlabel('Relative support')
    ax.set_ylabel('Number of frequent patterns')
    ax.grid(True)
    pylab.savefig(config.OUTPUT+"apriori_closed_itemset_count.pdf")
    
            


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

   
if __name__ == "__main__":
    files, support = read_opts(sys.argv[1:])
    analyse_clickstream(files, support)