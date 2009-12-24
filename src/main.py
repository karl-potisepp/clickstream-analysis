# -*- coding: utf_8 -*-
import sys, getopt, os

import apachelogs, logparser
import apriori, statistics, tree, fsm_wrapper
import time_decorator
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
    
    # sessions from the parser    

    transactions = [session for session in parser.get_simple_sessions() if config.filter_fn(session)]
    #stats.session_len_graph(parser.get_simple_sessions())
    #stats.page_freq_graph(parser.get_simple_sessions())
    db_size = len(transactions)
    print "db size after reduction:", db_size
    
    # if support is given as a float, it is presumed to be relative support
    # i.e. the minimum percentage of transactions to have a certain itemset
    # the percentage is then converted into absolute support
    if type(support) is float:
        min_support = int(len(transactions) * support)
    else:
        min_support = support
    
    print "Support", support


    # output all sessions into a file
    # row format : "page1" "page2" "page3" ... "pageN"
    """
    sessions_file = open(config.OUTPUT+"sessions.txt", 'w')
    for session in transactions:
        line = ",".join(session) + '\n'
        sessions_file.write(line)



    results = fsm_wrapper.fpm(transactions, min_support)
    times = time_decorator.deocarate_timings(results, parser, len(transactions))
    print "Sequential patterns: "
    for r in  results:
        print "\t",r
    
    
    lrs, mfs = tree.large_reference_sequences(transactions, min_support)
    times = time_decorator.deocarate_timings(lrs, parser)
    print "Large reference sequences: "
    for r in  lrs:
        print "\t",r
    
    """
    print "Apriori and closed itemset: "
    
    print "\n\n\n\n\n\n"
    print "\\begin{tabular}{ r | l }"
    print "Support & frequent itemset \\\\ \\hline"
    import operator
    data = apriori.extract_itemsets(transactions, min_support)
    data = sorted(data, key=operator.itemgetter(1), reverse=True)
    for itemset, support in data:
        s = 1.0*support / db_size
        print round(s,2), "&", 
        print ", ".join(itemset), 
        print "\\\\ \\hline"

    print "\\end{tabular}"
    print "\n\n\n\n\n\n"



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