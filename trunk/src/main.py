# -*- coding: utf_8 -*-
import sys, getopt, os

import apachelogs, logparser
import apriori, statistics
import config


def analyse_clickstream(paths, support):

    # read log files
    log = apachelogs.ApacheLogFile(*paths)

    # parse log files, extract sessions
    parser = logparser.LogParser(log, [])
    parser.parse()
    
    # output simple statistics about data set
    stats = statistics.LogFileStatistics(parser)
    stats.output_some_statistics()
    

    # if support is given as a float, it is presumed to be relative support
    # i.e. the minimum percentage of transactions to have a certain itemset
    # the percentage is then converted into absolute support
    if type(support) is float:
        min_support = int(parser.get_session_count() * support)
    else:
        min_support = support
    
    # sessions from the parser    
    transactions = [session for session in parser.get_simple_sessions() ]

    
    print "="*80
    # extract all itemsets with support => min_support
    rules = apriori.extract_itemsets(transactions, min_support)
    # find supports for itemsets from last step
    items = apriori.calculate_supports(rules, transactions)
    # print supports
    for n, itemset in items:
        print n, itemset
    print "="*80
    
    
    from fpgrowth import find_frequent_itemsets
    items = find_frequent_itemsets(transactions, min_support)
    for itemset in items:
        print itemset
    
"""
def output_stats():    
    import pylab
    lens = sorted([len(session) for session in transactions])
    pylab.hist(lens,bins=(range_max-range_min), range=(range_min,range_max))
    pylab.show()
"""


def read_opts(argv):
    filelist = config.paths
    logfile = None
    support = config.support    
    try:
        opts, args = getopt.getopt(argv, 's:', ["support"])
        if len(args) == 1:
            logfile = args[0]
        
        support = config.support
        for o, a in opts:
            #support
            if o in ("-s", "--support"):
                if a.find(".")!=-1:
                    support = float(a)
                    if support > 1.0:
                        raise getopt.GetoptError("support cannot be bigger than 1.0") 
                else:
                    support = int(a)
            else:
                raise getopt.GetoptError("incompatible arguments")


    except getopt.GetoptError, err:
        print "Error: " + str(err)
        sys.exit(2)    
    
    if logfile is not None and os.path.isdir(logfile) :
        filelist = map(lambda x: os.path.join(logfile, x), os.listdir(logfile))
        filelist = filter(lambda x: os.path.isfile(x), filelist)
    elif logfile is not None:
        filelist = [logfile]

    return filelist, support

        
            
    

if __name__ == "__main__":
    files, support = read_opts(sys.argv[1:])

    analyse_clickstream(files, support)


    
